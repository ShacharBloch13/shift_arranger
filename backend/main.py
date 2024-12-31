from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, add_availability, worker_availability, shifts, days
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from logic_flow import worker_availability, required_workers


app = FastAPI()


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
        add_availability(
            availability.worker, availability.day, availability.shift, availability.available
        )
    return {"status": "success"}


@app.get("/assign_shifts")
def assign_shifts():
    result = all_workers_submitted()
    if result is not True:
        notSubmitted = ', '.join(result)  
        return {

            "error": "Some workers have not submitted their availability : " + notSubmitted,
        }
    print('worker_availability:', worker_availability)  # Print the availability to the console
    assignments = generate_and_evaluate_assignments(50000)
    if not assignments:
        return {"error": "No valid assignments found."}

    best_assignment = max(assignments, key=lambda x: x[0])[1]

    serialized_assignment = {
        f"{day} {shift}": worker for (day, shift), worker in best_assignment.items()
    }

    return {"assignments": serialized_assignment, "score": fitness(best_assignment)}


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
