import pytest
tasks = []

def add_task(task):
    if not task:
      raise ValueError("Task cannot be empty.")
    else:
      tasks.append(task)
    return tasks

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return tasks
    else:
        return "Task not found."

def list_tasks():
    return tasks

def clear_tasks():
    tasks.clear()
    return "Tasks cleared."

def test_add_task():
    clear_tasks()
    assert add_task('Buy groceries') == ['Buy groceries']
    assert add_task('Read a book') == ['Buy groceries', 'Read a book']
    clear_tasks()

def test_list_tasks():
    clear_tasks()
    assert list_tasks() == []
    add_task('Buy groceries')
    assert list_tasks() == ['Buy groceries']
    add_task('Go for a run')
    assert list_tasks() == ['Buy groceries', 'Go for a run']
    clear_tasks()

@pytest.mark.parametrize("task, expected", [
    ('Buy groceries', ['Buy groceries']),
    ('Read a book', ['Buy groceries', 'Read a book']),
    ('Exercise', ['Buy groceries', 'Read a book', 'Exercise'])
])
def test_add_task_param(task, expected):
    assert add_task(task) == expected


# Additional Tests
def test_add_empty_task():
    clear_tasks()
    with pytest.raises(ValueError, match="Task cannot be empty."):
        add_task("")

def test_remove_existing_task():
    clear_tasks()
    add_task('Buy groceries')
    assert remove_task('Buy groceries') == []
    assert list_tasks() == []

def test_remove_non_existent_task():
    clear_tasks()
    assert remove_task('Non-existent task') == "Task not found."

def test_clear_tasks():
    add_task('Buy groceries')
    add_task('Read a book')
    assert clear_tasks() == "Tasks cleared."
    assert list_tasks() == []

def test_add_duplicate_task():
    clear_tasks()
    assert add_task('Buy groceries') == ['Buy groceries']
    assert add_task('Buy groceries') == ['Buy groceries', 'Buy groceries']
