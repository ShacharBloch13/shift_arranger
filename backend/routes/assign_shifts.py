
from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, worker_availability
from sqlalchemy.orm import Session
from db import SessionLocal, Assignment
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def assign_shifts(db: Session = Depends(get_db)):
    result = all_workers_submitted()
    if result is not True:
        notSubmitted = ', '.join(result)
        return {
            "error": f"Some workers have not submitted their availability: {notSubmitted}",
        }

    assignments = generate_and_evaluate_assignments(50000)
    if not assignments:
        return {"error": "No valid assignments found."}

    # Extract the best assignment and its score
    sorted_assignments = sorted(assignments, key=lambda x: x[0], reverse=True)


    # Convert tuple keys to strings for JSON compatibility
    serialized_assignments = [
        {
            "score": score,
            "assignments": {f"{day} {shift}": worker for (day, shift), worker in assignment.items()}
        }
        for score, assignment in sorted_assignments
    ]

    print("Serialized Assignment Data:", serialized_assignments)  # Debugging

    # Save to the database
    # db_record = Assignment(
    #     assignments=assignment_data_serialized,  # Use the serialized dictionary
    #     grade=score,  # Use the score
    #     SaturdayNight=assignment_data_serialized.get("Saturday 23:00-07:00")  # Extract the Saturday night worker
    # )
    # db.add(db_record)
    # db.commit()
    # db.refresh(db_record)

    return {"assignments_list": serialized_assignments}
