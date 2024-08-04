# shift_arranger
This is the first version of this project. V2 is expected to include a login option for all the users, DB usage etc.

Check out a short video depicting the project here:
```
https://youtu.be/O9g5oMY02dg
```
This project is a full-stack application developed with FastAPI, designed to help schedule worker shifts based on their availability. The application collects availability data from workers and generates optimized shift assignments using a custom algorithm.

# Features
1. Workers can submit their availability for various shifts throughout the week.
2. Generate optimized shift assignments based on workers' availability and constraints.
3. Display the generated assignments in a user-friendly table format.

# Technology Used
1. Backend: FastAPI
2. Frontend: HTML, CSS, JavaScript

# Installation
```
git clone https://github.com/ShacharBloch13/shift_arranger.git
cd shift-scheduler

```
# Backend Setup
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
1. Start the backend server:
```
uvicorn main:app --reload
```
2. Open the browser and go to localhost:8000 to access the application.

# Project Structure
```
worker-shift-scheduler/
│
├── backend/
│   ├── __pycache__/
│   ├── .pytest_cache/
│   ├── main.py
│   ├── logic_flow.py
│   └── requirements.txt
│
├── frontend/
│   ├── design.html
│   ├── styles.css
│
├── .gitignore
└── README.md
```
# Backend Implementation

# main.py
The main.py file sets up the FastAPI application, defines routes, and serves static files. Key routes include:
1. /set_availability: Accepts POST requests with workers' availability data.
2. /assign_shifts: Generates and returns optimized shift assignments.

# logic_flow.py
The logic_flow.py file contains the core algorithm for generating and evaluating shift assignments. Key functions include:
1. add_availability(worker, day, shift): Updates the availability data for a worker.
2. all_workers_submitted(): Checks if all workers have submitted their availability.
3. generate_valid_assignment(): Generates a valid shift assignment considering constraints such as maximum night shifts and minimum shifts per worker.
4. fitness(individual): Evaluates the quality of a shift assignment.
5. generate_and_evaluate_assignments(num_assignments): Generates and evaluates multiple shift assignments to find the best one.

# Algorithm Details

1. constraints:
   1.1. Maximum of 1 night shift per worker per week.
   1.2. Minimum of 2 shifts and maximum of 3 shifts per worker per week.
2. Fitness Evaluation:
   2.1. Starts with a perfect score of 100.
   2.2. Deducts points for consecutive shifts and other violations.
   2.3. Ensures a balanced and fair distribution of shifts.
3. Assignment Generation:
   3.1. Randomly assigns workers to shifts based on availability.
   3.2. Ensures constraints are met and the solution is optimized for fairness.

# Conributing

I welcome contributions to this project! Whether you want to add new features, improve existing functionality, or fix bugs, your help is appreciated. Please feel free to fork the repository and submit pull requests.

Thank you for checking out this project. If you have any questions or suggestions, please feel free to open an issue or contact us directly. Happy coding!
   
