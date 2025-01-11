from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal, Assignment
import logic_flow
from datetime import datetime

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
        manager = logic_flow.manager
        currenttime = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a new assignment record
        new_assignment = Assignment(
            id=f"{manager}_{currenttime}",
            assignments=assignment.assignments,
            grade=assignment.score,
            SaturdayNight=assignment.assignments.get("Saturday 23:00-07:00"),
            manager=logic_flow.manager
        )
        db.add(new_assignment)
        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
