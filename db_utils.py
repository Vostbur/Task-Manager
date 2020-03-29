import os
import sqlite3
from collections import namedtuple


class DataBase:
    """Class for common database operations """
    db_schema_filename = 'task_manager_schema.sql'

    def __init__(self):
        db_filename = 'db.db'
        self.db_exists = os.path.exists(db_filename)
        self.conn = sqlite3.connect(db_filename, check_same_thread=False)
        self.project = namedtuple('project', 'project_id name active')
        self.task = namedtuple('task', 'task_id project name date status')

    def get_items(self, item):
        return list(map(lambda row, self=self: eval('self.{}(*row)'.format(item)),
                    self.conn.execute('select * from {}'.format(item))))

    def get_item(self, item, item_id):
        row = next(self.conn.execute('select * from {} where id = :id'.format(item), {'id': item_id}))
        return eval('self.{}(*row)'.format(item))

    def delete_item(self, item, field, item_id):
        with self.conn:
            self.conn.execute('delete from {} where {} = :id'.format(item, field), {'id': item_id})

    def update_item(self, item, item_id, field, state):
        with self.conn:
            self.conn.execute('update {} set {} = :state where id = :id'.format(item, field),
                              {'state': state, 'id': item_id})

    def add_project(self, project):
        with self.conn:
            self.conn.execute('insert into project (name) values (?)', (project,))

    def add_task(self, project_id, task, date, status):
        with self.conn:
            self.conn.execute('insert into task (project, name, date, status) \
                              values (?, ?, ?, ?)',
                              (project_id, task, date, status))

    def create_schema(self):
        if self.db_exists:
            return
        with self.conn, open(self.db_schema_filename) as schema:
            self.conn.executescript(schema.read())
