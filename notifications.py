import schedule
import time
import threading
from tkinter import messagebox
from tasks_controller import handle_get_tasks
from datetime import datetime, timedelta

# Funcție pentru a verifica dacă un task are nevoie de un reminder
def check_reminders(root):
    tasks = handle_get_tasks()
    current_time = datetime.now()
    
    for task in tasks:
        due_date_str = task[5]  # Data limită a sarcinii
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
        time_left = due_date - current_time

        if timedelta(hours=1) >= time_left >= timedelta(minutes=0):
            messagebox.showinfo("Memento pentru sarcină", f"Sarcina '{task[1]}' are termen limită la {due_date.strftime('%Y-%m-%d %H:%M')}!")

# Funcție pentru a rula programarea memento-urilor într-un thread separat
def run_schedule(root):
    while True:
        schedule.run_pending()
        time.sleep(1)

# Funcție pentru a programa verificarea memento-urilor la fiecare minut
def schedule_reminders(root):
    tasks = handle_get_tasks()

    for task in tasks:
        due_date_str = task[5]
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S')
            reminder_time = due_date - timedelta(hours=1)

            if reminder_time > datetime.now():
                schedule.every().day.at(reminder_time.strftime('%H:%M')).do(check_reminders, root)
        except ValueError:
            print(f"Formatul datei '{due_date_str}' este incorect sau lipsit!")

    # Pornim thread-ul pentru memento-uri
    reminder_thread = threading.Thread(target=run_schedule, args=(root,))
    reminder_thread.daemon = True  # Thread-ul daemon se va opri odată cu închiderea aplicației
    reminder_thread.start()
