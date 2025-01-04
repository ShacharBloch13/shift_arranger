from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, add_availability, worker_availability, shifts, days
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.assign_shifts import router as assignments_router
from routes.set_availability import router as set_availability_router
from routes.accept_assignments import router as accept_assignment_router


app = FastAPI()


class Availability(BaseModel):
    worker: str
    day: str
    shift: str
    available: bool

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
templates = Jinja2Templates(directory="../frontend")

app.include_router(set_availability_router, prefix="/availability", tags=["Availability"])
app.include_router(assignments_router, prefix="/assignments", tags=["Assignments"])
app.include_router(accept_assignment_router, prefix="/assignments", tags=["Accept Assignment"])

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("design.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
