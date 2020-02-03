# -*- coding: utf-8 -*-
import csv
import os
import sys

#### Insert test data ######
csv_project = "data_project.csv"
csv_task = "data_task.csv"
if not os.path.exists(csv_project) or not os.path.exists(csv_task):
    sys.exit(1)
query_insert_project = """insert into project (name, active)
values (:name, :active)
"""
query_insert_task = """insert into task (project, name, date)
values (:project, :name, :date)
"""
with open(csv_project) as project, open(csv_task) as task:
    project_from_csv = csv.DictReader(project)
    self.write_data_to_table(query_insert_project, project_from_csv)
    task_from_csv = csv.DictReader(task)
    self.write_data_to_table(query_insert_task, task_from_csv)
#### end test code fragment #####
