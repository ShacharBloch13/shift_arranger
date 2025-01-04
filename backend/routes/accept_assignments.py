from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal, Assignment

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AcceptedAssignment(BaseModel):
    assignments: dict
    score: int

@router.post("/accept")
async def accept_assignment(assignment: AcceptedAssignment, db: Session = Depends(get_db)):
    try:
        # Create a new assignment record
        new_assignment = Assignment(
            assignments=assignment.assignments,
            grade=assignment.score,
            SaturdayNight=assignment.assignments.get("Saturday 23:00-07:00")
        )
        db.add(new_assignment)
        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
