from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1


@app.get("/tasks")
def get_tasks(priority: int = None):
    # If a priority query parameter is provided, validate and filter
    if priority is not None:
        if priority < 1 or priority > 3:
            raise HTTPException(status_code=400, detail="Priority must be between 1 and 3")
        
        # Return a filtered list of tasks that match the requested priority
        filtered_tasks = []
        for task in tasks:
            if task.get("priority") == priority:
                filtered_tasks.append(task)
        return filtered_tasks
        
    # If no priority was provided, return all tasks
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    
    # Extract priority, defaulting to 2 if it was not provided
    priority = task.get("priority", 2)
    
    # Validate the priority is an integer and within the 1-3 range
    if not isinstance(priority, int) or priority < 1 or priority > 3:
        raise HTTPException(status_code=400, detail="Priority must be a number between 1 and 3")
        
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority 
    }
    
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")