# -*- coding: utf-8 -*-
"""
@author: Рубцов
for PEP8 check use: python -m pycodestyle app.py
"""

from datetime import datetime as dt
from flask import Flask, request, Response, abort, redirect
from flask import render_template
from flask_login import LoginManager, login_required, UserMixin
from flask_login import login_user, current_user
import db_utils as d

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

db = d.DataBase()
db.create_schema()


class User(UserMixin):

    def __init__(self, username, password, id, active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return self.make_secure_token(self.username, key='secret_key')


class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier += 1
        return self.identifier


users_repository = UsersRepository()


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
        user = "Не зарегистрирован"

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
    else:
        db.set_task_status(task_id, 1)

    return redirect('/')


@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    """Delete task """
    task = db.get_task_by_id(task_id)

    if not task:
        return redirect('/')

    db.delete_task(task_id)
    return redirect('/')


@app.route('/clear/<delete_id>')
@login_required
def clear_all(delete_id):
    """Delete project with tasks """
    db.delete_project(delete_id)
    db.delete_tasks_in_project(delete_id)
    return redirect('/')


@app.route('/remove/<lists_id>')
@login_required
def remove_all(lists_id):
    """Delete all tasks in project """
    db.delete_tasks_in_project(lists_id)
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        registeredUser = users_repository.get_user(username)
        if registeredUser is not None and registeredUser.password == password:
            print('Logged in..')
            login_user(registeredUser)
            return redirect('/')
        else:
            return abort(401)
    else:
        return Response('''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        ''')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password, users_repository.next_index())
        users_repository.save_user(new_user)
        return Response(
                '''<p>Пользователь зарегистрирован</p>
                <br /><a href="/">Вернуться</a>'''
                )
    else:
        return Response('''
            <form action="" method="post">
            <p><input type=text name=username placeholder="Enter username">
            <p><input type=password name=password placeholder="Enter password">
            <p><input type=submit value=Login>
            </form>
        ''')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p><br /><a href="/">Вернуться</a>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
