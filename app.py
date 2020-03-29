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
    projects = db.get_items('project')
    tasks = db.get_items('task')

    if projects:
        for project in projects:
            if project.active:
                active = project.project_id
        if not active:
            active = projects[0].project_id
            db.update_item('project', projects[0].project_id, 'active', 1)
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
        project = 'Default project'

    projects = db.get_items('project')
    for proj in projects:
        if proj.name == project:
            found = True
            break

    if not found:
        db.add_project(project)
        logger.info('Пользователь "{}" создал проект "{}".'.format(current_user.username, project))
        projects = db.get_items('project')

    for proj in projects:
        if proj.name == project:
            project_id = proj.project_id
        db.update_item('project', proj.project_id, 'active', int(proj.name == project))

    status = 1 if bool(int(request.form['status'])) else 0
    date = dt.strftime(dt.now(), "%d.%m.%Y")
    db.add_task(project_id, task, date, status)
    logger.info('Пользователь "{}" добавил задачу "{}".'.format(current_user.username, task))
    return redirect('/')


@app.route('/close/<int:task_id>')
@login_required
def close_task(task_id):
    """Close task """
    task = db.get_item('task', task_id)
    if task:
        db.update_item('task', task_id, 'status', abs(task.status-1))
        logger.info('Пользователь "{}" изменил статус задачи "{}".'.format(current_user.username, task.name))
    return redirect('/')


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """Delete task """
    task = db.get_item('task', task_id)
    if task:
        db.delete_item('task', 'id', task_id)
        logger.info('Пользователь "{}" удалил задачу "{}".'.format(current_user.username, task.name))
    return redirect('/')


@app.route('/clear/<project_id>')
@login_required
def clear_all(project_id):
    """Delete project with tasks """
    project = db.get_item('project', project_id)
    db.delete_item('task', 'project', project_id)
    db.delete_item('project', 'id', project_id)
    logger.info('Пользователь "{}" удалил проект "{}".'.format(current_user.username, project.name))
    return redirect('/')


@app.route('/remove/<project_id>')
@login_required
def remove_all(project_id):
    """Delete all tasks in project """
    project = db.get_item('project', project_id)
    db.delete_item('task', 'project', project_id)
    logger.info('Пользователь "{}" удалил все задачи из проекта "{}".'.format(current_user.username, project.name))
    return redirect('/')


@app.route('/project/<tab>')
def tab_nav(tab):
    """Change active project """
    projects = db.get_items('project')
    for project in projects:
        db.update_item('project', project.project_id, 'active', int(project.name == tab))
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        registered_user = users_repository.get_user(username)
        if registered_user is not None and registered_user.password == password:
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
