# -*- coding: utf-8 -*-
"""
@author: Рубцов
for PEP8 check use: python -m pycodestyle app.py
"""
from datetime import datetime as dt
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import db_utils as d

app = Flask(__name__)

db = d.DataBase()
db.create_schema()


@app.route('/')
def index():
    """Route for main page """
    active = None
    projects = db.get_projects()
    tasks = db.get_tasks()

    if projects:
        for project in projects:
            if project[2]:
                active = project[0]
        if not active:
            active = projects[0][0]
            db.update_active_project(projects[0][0], 1)
    else:
        projects = None

    if projects:
        return render_template('index.html', tasks=tasks, projects=projects,
                               active=active)
    return render_template('index.html', tasks=tasks, active=active)


@app.route('/add', methods=['POST'])
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
        if proj[1] == project:
            found = True
            break

    if not found:
        db.add_project(project)
        projects = db.get_projects()

    for proj in projects:
        if proj[1] == project:
            project_id = proj[0]
            db.update_active_project(proj[0], 1)
        else:
            db.update_active_project(proj[0], 0)

    status = 1 if bool(int(request.form['status'])) else 0

    date = dt.strftime(dt.now(), "%d.%m.%Y")
    db.add_task(project_id, task, date, status)
    return redirect('/')


@app.route('/close/<int:task_id>')
def close_task(task_id):
    """Close task """
    task = db.get_task_by_id(task_id)

    if not task:
        return redirect('/')

    if task[4]:
        db.set_task_status(task_id, 0)
    else:
        db.set_task_status(task_id, 1)

    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete task """
    task = db.get_task_by_id(task_id)

    if not task:
        return redirect('/')

    db.delete_task(task_id)
    return redirect('/')


@app.route('/clear/<delete_id>')
def clear_all(delete_id):
    """Delete project with tasks """
    db.delete_project(delete_id)
    db.delete_tasks_in_project(delete_id)
    return redirect('/')


@app.route('/remove/<lists_id>')
def remove_all(lists_id):
    """Delete all tasks in project """
    db.delete_tasks_in_project(lists_id)
    return redirect('/')


@app.route('/project/<tab>')
def tab_nav(tab):
    """Change active project """
    projects = db.get_projects()

    for project in projects:
        if project[1] == tab:
            db.update_active_project(project[0], 1)
        else:
            db.update_active_project(project[0], 0)

    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
