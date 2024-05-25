from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, add_availability
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Define shifts and days
shifts = ['07:00-15:00', '15:00-23:00', '23:00-07:00']
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# List of all worker names
required_workers = ["Worker1", "Worker2", "Worker3", "Worker4", "Worker5", "Worker6", "Worker7"]
worker_availability = {worker: {day: {shift: False for shift in shifts} for day in days} for worker in required_workers}

class Availability(BaseModel):
    worker: str
    day: str
    shift: str
    available: bool

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
templates = Jinja2Templates(directory="../frontend")

@app.post("/set_availability")
async def set_availability(availabilities: List[Availability]):
    for availability in availabilities:
        add_availability(availability.worker, availability.day, availability.shift)
    print('worker_availability:')
    print(worker_availability)  # Print the availability to the console
    return {"status": "success"}

@app.get("/assign_shifts")
def assign_shifts():
    if all_workers_submitted():
        print('passed all workers submitted')

        assignments = generate_and_evaluate_assignments(50000)
        if not assignments:
            return {"error": "No valid assignments found."}

        best_assignment = max(assignments, key=lambda x: x[0])[1]
        
        # Convert the assignments to a serializable format
        serialized_assignment = {
            f"{day} {shift}": worker for (day, shift), worker in best_assignment.items()
        }

        return {"assignments": serialized_assignment, "score": fitness(best_assignment)}
    else:
        return {"error": "Not all workers have submitted their availability."}

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
