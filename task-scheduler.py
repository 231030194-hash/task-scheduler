import json
import schedule
import time
from datetime import datetime

TASK_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task():
    task = input("Enter task description: ")
    priority = input("Priority (High/Medium/Low): ")
    deadline = input("Deadline (YYYY-MM-DD): ")

    tasks = load_tasks()
    tasks.append({
        "task": task,
        "priority": priority,
        "deadline": deadline,
        "status": "Pending"
    })
    save_tasks(tasks)
    print("Task added successfully!")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks available.")
        return

    print("\n----- Today's Tasks -----")
    for idx, t in enumerate(tasks, 1):
        print(f"{idx}. {t['task']} | Priority: {t['priority']} | Deadline: {t['deadline']} | Status: {t['status']}")
    print("--------------------------\n")

def mark_complete():
    tasks = load_tasks()
    view_tasks()
    task_no = int(input("Enter task number to mark complete: "))
    tasks[task_no - 1]["status"] = "Completed"
    save_tasks(tasks)
    print("Task marked as complete!")

def reset_tasks():
    print("Resetting all tasks for a new day...")
    tasks = load_tasks()
    for t in tasks:
        t["status"] = "Pending"
    save_tasks(tasks)
    print("Daily reset complete!")

# Schedule daily reset at midnight
schedule.every().day.at("00:00").do(reset_tasks)

def menu():
    while True:
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_complete()
        elif choice == "4":
            break
        else:
            print("Invalid choice!")

        # run scheduled tasks
        schedule.run_pending()
        time.sleep(1)

menu()
