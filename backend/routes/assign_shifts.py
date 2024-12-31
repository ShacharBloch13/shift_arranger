
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, worker_availability

router = APIRouter()

@router.get("/")
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
