# -*- coding: utf-8 -*-
"""
Test:
sqlite3 db.db "select name from sqlite_master where type='table'"
sqlite3 db.db "select * from task"

for PEP8 check use: python -m pycodestyle db_utils.py
"""

import os
import sqlite3
from collections import namedtuple
import log_lib


# Настройка логгирования
app_logger = log_lib.get_logger('db.log')


class DataBase:
    """Class for common database operation """
    db_schema_filename = "task_manager_schema.sql"

    def __init__(self):
        db_filename = "db.db"
        self.db_exists = os.path.exists(db_filename)
        self.conn = sqlite3.connect(db_filename,
                                    check_same_thread=False)
        self.Project = namedtuple("Project", "project_id name active")
        self.Task = namedtuple("Task", "task_id project name date status")

    def write_data_to_table(self, query, data):
        """Write data to table """
        try:
            self.conn.executemany(query, data)
        except Exception as err:
            print(err)
            self.conn.rollback()
            raise err
        else:
            self.conn.commit()

    def get_projects(self):
        """Get projects."""
        projects = []
        for row in self.conn.execute("select * from project"):
            projects.append(self.Project(project_id=row[0], name=row[1],
                                         active=row[2]))
        return projects

    def get_tasks(self):
        """Get tasks """
        tasks = []
        for row in self.conn.execute("select * from task"):
            tasks.append(self.Task(task_id=row[0], project=row[1], name=row[2],
                                   date=row[3], status=row[4]))
        return tasks

    def get_task_by_id(self, task_id):
        """Get task by ID """
        row = list(self.conn.execute("select * from task where id=?;",
                                     (task_id,)))[0]
        return self.Task(task_id=row[0], project=row[1], name=row[2],
                         date=row[3], status=row[4])

    def set_task_status(self, task_id, status):
        """Set task status """
        with self.conn:
            self.conn.execute("update task set status=? where id=?;",
                              (status, task_id))
        app_logger.debug(f'Update status task - {task_id}')

    def delete_task(self, task_id):
        """Delete task """
        with self.conn:
            self.conn.execute("delete from task where id=?;", (task_id,))

    def delete_tasks_in_project(self, project_id):
        """Filter and delete task """
        with self.conn:
            self.conn.execute("delete from task where project=?;",
                              (project_id,))

    def delete_project(self, project_id):
        """Delete project """
        with self.conn:
            self.conn.execute("delete from project where id=?;", (project_id,))

    def update_active_project(self, project_id, flag):
        """Update project """
        with self.conn:
            self.conn.execute("update project set active=? where id=?;",
                              (flag, project_id))

    def add_project(self, project):
        """Add project """
        with self.conn:
            self.conn.execute("insert into project (name) \
                              values (?)", (project,))

    def add_task(self, project_id, task, date, status):
        """Add task """
        with self.conn:
            self.conn.execute("insert into task (project, name, date, status) \
                              values (?, ?, ?, ?)",
                              (project_id, task, date, status))

    def create_schema(self):
        """Create schema """
        if self.db_exists:
            return
        with self.conn, open(self.db_schema_filename) as fname:
            self.conn.executescript(fname.read())
