tasks = []

def add_task(task):
    tasks.append(task)
    return f"Task '{task}' added."

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        return f"Task '{task}' removed."
    else:
        return "Task not found."

def list_tasks():
    return tasks

# Example usage
# print(add_task("Buy groceries"))
# print(add_task("Read a book"))
# print(list_tasks())
# print(remove_task("Read a book"))
# print(list_tasks())


# LLM Testing
# Test Case 1: Add a Task
print(add_task("Do laundry"))
print(list_tasks())  # Expected: ["Do laundry"]

# Test Case 2: Remove a Task
print(add_task("Clean the house"))
print(remove_task("Clean the house"))
print(list_tasks())  # Expected: []

# Test Case 3: Remove a Non-Existent Task
print(remove_task("Go jogging"))  # Expected: "Task not found."

# Test Case 4: Add Duplicate Tasks
print(add_task("Read a book"))
print(add_task("Read a book"))
print(list_tasks())  # Expected: ["Read a book", "Read a book"]

# Test Case 5: List Tasks When Empty
tasks.clear()  # Resetting the task list to empty
print(list_tasks())  # Expected: []

# Test Case 6: Add Task with Special Characters
print(add_task("Pay bills @ bank #1"))
print(list_tasks())  # Expected: ["Pay bills @ bank #1"]

# Test Case 7: Add an Empty Task
print(add_task(""))  # Depending on the implementation, this might add an empty task
print(list_tasks())  # Expected: [""] if empty tasks are allowed; otherwise, [] if they are not allowed