from database import add_task, get_tasks, delete_task, update_task, get_task_statistics, archive_task

def handle_add_task(title, description, category, subcategory, due_date, priority, status, reminder):
    add_task(title, description, category, subcategory, due_date, priority, status, reminder)

def handle_get_tasks(filter_by=None, search_query=None):
    return get_tasks(filter_by, search_query)

def handle_delete_task(task_id):
    delete_task(task_id)

def handle_update_task(task_id, title, description, category, subcategory, due_date, priority, status):
    update_task(task_id, title, description, category, subcategory, due_date, priority, status)

def handle_archive_task(task_id):
    archive_task(task_id)

def handle_get_statistics():
    return get_task_statistics()
