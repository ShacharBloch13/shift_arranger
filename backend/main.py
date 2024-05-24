from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from logic_flow import generate_and_evaluate_assignments, fitness, all_workers_submitted, add_availability
import uvicorn

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
async def get_form():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shift Availability</title>
        <script>
            async function submitAvailability() {
                let availabilities = [];
                document.querySelectorAll('.availability').forEach((checkbox) => {
                    let [worker, day, shift] = checkbox.id.split('_');
                    availabilities.push({
                        worker: worker,
                        day: day,
                        shift: shift,
                        available: checkbox.checked
                    });
                });
                let response = await fetch('/set_availability', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(availabilities)
                });
                let result = await response.json();
                alert(result.status);
            }

            async function getAssignments() {
                let response = await fetch('/assign_shifts');
                let result = await response.json();
                if (result.error) {
                    alert(result.error);
                } else {
                    document.getElementById('assignments').innerHTML = JSON.stringify(result.assignments, null, 2);
                    document.getElementById('score').innerText = 'Score: ' + result.score;
                }
            }
        </script>
    </head>
    <body>
        <h1>Shift Availability</h1>
        <form onsubmit="event.preventDefault(); submitAvailability();">
            <table border="1">
                <thead>
                    <tr>
                        <th>Worker</th>
                        <th>Day</th>
                        <th>Shift</th>
                        <th>Available</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Dynamically generate the form fields -->
                    <script>
                        const workers = ["Worker1", "Worker2", "Worker3", "Worker4", "Worker5", "Worker6", "Worker7"];
                        const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                        const shifts = ["07:00-15:00", "15:00-23:00", "23:00-07:00"];
                        
                        workers.forEach(worker => {
                            days.forEach(day => {
                                shifts.forEach(shift => {
                                    document.write(`
                                        <tr>
                                            <td>${worker}</td>
                                            <td>${day}</td>
                                            <td>${shift}</td>
                                            <td><input type="checkbox" id="${worker}_${day}_${shift}" class="availability"></td>
                                        </tr>
                                    `);
                                });
                            });
                        });
                    </script>
                </tbody>
            </table>
            <button type="submit">Submit Availability</button>
        </form>
        <button onclick="getAssignments()">Get Assignments</button>
        <h2>Assignments</h2>
        <pre id="assignments"></pre>
        <p id="score"></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
