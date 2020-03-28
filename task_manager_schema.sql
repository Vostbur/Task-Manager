-- Схема для приложения task_manager

-- Проекты
create table project (
    id      integer primary key autoincrement not null,
    name    text not NULL,
    active  integer
);

-- Задачи в проектах
create table task (
    id      integer primary key autoincrement not null,
    project integer not null references project(id),
    name    text not NULL,
    date    text,
    status  integer default 0
);
