import hashlib
from datetime import datetime as dt

from flask import Flask, request, Response, redirect
from flask import render_template
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, current_user

import db_utils as d
from loguru import logger
from user_lib import User, UsersRepository

DEBUG = True

# Настрока flask приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Настройка базы данных проектов и задач
db = d.DataBase()
db.create_schema()

# Настройка авторизации
users_repository = UsersRepository()

# Настройка логгирования
logger.add("log.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="20 MB")


@app.route('/')
def index():
    """Route for main page """
    active = None
    projects = db.get_projects()
    tasks = db.get_tasks()

    if projects:
        for project in projects:
            if project.active:
                active = project.project_id
        if not active:
            active = projects[0].project_id
            db.update_active_project(projects[0].project_id, 1)
    else:
        projects = None

    try:
        user = current_user.username
    except AttributeError:
        user = False

    if projects:
        return render_template('index.html', tasks=tasks, projects=projects,
                               active=active, user=user)
    return render_template('index.html', tasks=tasks, active=active,
                           user=user)


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    """Add task """
    found = False
    project_id = None
    task = request.form['task']
    project = request.form['project']

    if not task:
        return redirect('/')

    if not project:
        project = 'Tasks'

    projects = db.get_projects()

    for proj in projects:
        if proj.name == project:
            found = True
            break

    if not found:
        db.add_project(project)
        logger.info('Пользователь "{}" создал проект "{}".'.format(current_user.username, project))
        projects = db.get_projects()

    for proj in projects:
        if proj.name == project:
            project_id = proj.project_id
            db.update_active_project(proj.project_id, 1)
        else:
            db.update_active_project(proj.project_id, 0)

    status = 1 if bool(int(request.form['status'])) else 0

    date = dt.strftime(dt.now(), "%d.%m.%Y")
    db.add_task(project_id, task, date, status)
    logger.info('Пользователь "{}" добавил задачу "{}".'.format(current_user.username, task))
    return redirect('/')


@app.route('/close/<int:task_id>')
@login_required
def close_task(task_id):
    """Close task """
    task = db.get_task_by_id(task_id)

    if not task:
        return redirect('/')

    if task.status:
        db.set_task_status(task_id, 0)
        logger.info('Пользователь "{}" отметил задачу "{}" как "выполнено".'.format(current_user.username, task.name))
    else:
        db.set_task_status(task_id, 1)
        logger.info('Пользователь "{}" отметил задачу "{}" как "не выполнено".'.format(current_user.username,
                                                                                       task.name))

    return redirect('/')


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """Delete task """
    task = db.get_task_by_id(task_id)

    if not task:
        return redirect('/')

    db.delete_task(task_id)
    logger.info('Пользователь "{}" удалил задачу "{}".'.format(current_user.username, task.name))
    return redirect('/')


@app.route('/clear/<delete_id>')
@login_required
def clear_all(delete_id):
    """Delete project with tasks """
    project = db.get_name_project_by_id(delete_id)
    db.delete_project(delete_id)
    db.delete_tasks_in_project(delete_id)
    logger.info('Пользователь "{}" удалил проект "{}".'.format(current_user.username, project))
    return redirect('/')


@app.route('/remove/<lists_id>')
@login_required
def remove_all(lists_id):
    """Delete all tasks in project """
    project = db.get_name_project_by_id(lists_id)
    db.delete_tasks_in_project(lists_id)
    logger.info('Пользователь "{}" удалил все задачи из проекта "{}".'.format(current_user.username, project))
    return redirect('/')


@app.route('/project/<tab>')
def tab_nav(tab):
    """Change active project """
    projects = db.get_projects()

    for project in projects:
        if project.name == tab:
            db.update_active_project(project.project_id, 1)
        else:
            db.update_active_project(project.project_id, 0)

    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        registered_user = users_repository.get_user(username)
        if registered_user is not None \
                and registered_user.password == password:
            login_user(registered_user)
            logger.info('Пользователь "{}" начал работу'.format(username))
    return redirect('/')


@app.route('/logout', methods=['POST'])
def logout():
    out_user = current_user.username
    logout_user()
    logger.info('Пользователь "{}" закончил работу'.format(out_user))
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
    new_user = User(username, password, users_repository.next_index())
    users_repository.save_user(new_user)
    logger.info('Пользователь "{}" зарегистрирован'.format(username))
    return redirect('/')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p><br /><a href="/">Вернуться</a>')


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return users_repository.get_user_by_id(user_id)


if __name__ == '__main__':
    if DEBUG:
        app.run(host='127.0.0.1', debug=True)
    else:
        app.run(host='0.0.0.0', debug=False)
