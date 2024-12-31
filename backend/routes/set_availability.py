from logic_flow import add_availability
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

router = APIRouter()


class Availability(BaseModel):
    worker: str
    day: str
    shift: str
    available: bool

@router.post("/")
async def set_availability(availabilities: List[Availability]):
    for availability in availabilities:
        add_availability(
            availability.worker, availability.day, availability.shift, availability.available
        )
    return {"status": "success"}
