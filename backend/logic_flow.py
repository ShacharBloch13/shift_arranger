import random

# Define the constraints
MAX_NIGHT_SHIFTS = 1
MIN_SHIFTS = 2
MAX_SHIFTS = 3
NUM_ASSIGNMENTS = 50000

# Define shifts and days
shifts = ['07:00-15:00', '15:00-23:00', '23:00-07:00']
days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday','Saturday']

# List of all worker names
required_workers = ["Worker1", "Worker2", "Worker3", "Worker4", "Worker5","Worker6","Worker7"]
worker_availability = {worker: {day: {shift: False for shift in shifts} for day in days} for worker in required_workers}


# Availability setup for 7 days with 3 shifts per day for debugging
# worker_availability = {
#     "Worker1": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Tuesday": {'07:00-15:00': False, '15:00-23:00': True, '23:00-07:00': True},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Friday": {'07:00-15:00': False, '15:00-23:00': True, '23:00-07:00': True},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#     },
#     "Worker2": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Thursday": {'07:00-15:00': False, '15:00-23:00': True, '23:00-07:00': True},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#     },
#     "Worker3": {
#         "Sunday": {'07:00-15:00': False, '15:00-23:00': True, '23:00-07:00': True},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#     },
#     "Worker4": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#     },
#     "Worker5": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#     },
#     "Worker6": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#     },
#     "Worker7": {
#         "Sunday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Monday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Tuesday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Wednesday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Thursday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#         "Friday": {'07:00-15:00': True, '15:00-23:00': False, '23:00-07:00': True},
#         "Saturday": {'07:00-15:00': True, '15:00-23:00': True, '23:00-07:00': False},
#     }
# }


def add_availability(worker, day, shift, available):
    if worker in worker_availability:
        worker_availability[worker][day][shift] = available  # Respect the passed value
    else:
        print(f"Worker {worker} is not in the list of required workers.")


def all_workers_submitted():
    workers_with_no_availability = []

    for worker, days in worker_availability.items():
        all_false = all(not any(shifts.values()) for shifts in days.values())
        if all_false:
            workers_with_no_availability.append(worker)

    return True if not workers_with_no_availability else workers_with_no_availability


def generate_valid_assignment():
    individual = {}
    night_shift_count = {worker: 0 for worker in required_workers}

    for day in days:
        previous_day = days[(days.index(day) - 1) % len(days)] 
        previous_worker = None
        for shift in shifts:
            if shift == '07:00-15:00':
                previous_shift = '23:00-07:00'
            if shift == '15:00-23:00':
                previous_shift = '07:00-15:00'
            if shift == '23:00-07:00':
                previous_shift = '15:00-23:00'
            available_workers = [worker for worker in required_workers if worker_availability[worker][day][shift]]
            if shift == '23:00-07:00':
                available_workers = [worker for worker in available_workers if night_shift_count[worker] < MAX_NIGHT_SHIFTS]

            if previous_worker in available_workers:
                available_workers.remove(previous_worker)

            if (day != 'Sunday') and (shift == '07:00-15:00') and individual[(previous_day, '23:00-07:00')] in available_workers:
                available_workers.remove(individual[(previous_day, '23:00-07:00')])

            if available_workers:
                previous_worker = individual[previous_day, previous_shift] if (previous_day, previous_shift) in individual else available_workers[0]
                chosen_worker = random.choice(available_workers)
                individual[(day, shift)] = chosen_worker
                previous_worker = chosen_worker
                if shift == '23:00-07:00':
                    night_shift_count[chosen_worker] += 1
            else:
                return None  # Return None if no valid assignment can be made

    # Ensure minimum and maximum shifts constraints
    shift_count = {worker: 0 for worker in required_workers}
    for worker in individual.values():
        shift_count[worker] += 1

    for count in shift_count.values():
        if count < MIN_SHIFTS or count > MAX_SHIFTS:
            return None

    return individual

def fitness(individual):
    score = 100  # Start with a perfect score
    
    # Deduct points if a worker is assigned to 2 out of 3 consecutive shifts
    for day in days:
        for i in range(len(shifts) - 2):
            shift1, shift3 = shifts[i], shifts[i+2]
            if (individual[(day, shift1)] == individual[(day, shift3)]):
                score -= 10
    for i in range(len(days) - 1):
        day1, day2 = days[i], days[i+1]
        if (individual[(day1, '23:00-07:00')] == individual[(day2, '15:00-23:00')]) or (individual[(day1, '15:00-23:00')] == individual[(day2, '07:00-15:00')]):
            score -= 10
        if (individual[(day1, '23:00-07:00')] == individual[(day2, '07:00-15:00')]):
            score = 0
            

    return max(score, 0)  # Ensure score is not negative

def generate_and_evaluate_assignments(num_assignments):
    assignments = []
    for _ in range(num_assignments):
        individual = generate_valid_assignment()
        if individual:
            fit = fitness(individual)
            assignments.append((fit, individual))
            if fit == 100:
                break
    return assignments

def main():
    for worker in required_workers:
        print(f"\nEnter availability for {worker}:")
        for day in days:
            for shift in shifts:
                availability = input(f"Can you work on {day} during {shift}? (y/n): ").strip().lower()
                if availability == 'y':
                    add_availability(worker, day, shift)
    
    if all_workers_submitted():
        assignments = generate_and_evaluate_assignments(NUM_ASSIGNMENTS)
        if assignments:
            length = len(assignments)
            for i in range(0, length):
                print(assignments[i])
            best_assignment = max(assignments, key=lambda x: x[0])[1]
            print("\nBest shift assignments:")
            print("Score:", fitness(best_assignment))
            for key, value in best_assignment.items():
                print(f"Day: {key[0]}, Shift: {key[1]}, Worker: {value}")
        else:
            print("No valid assignments found.")
    else:
        notSubmitted = ', '.join(all_workers_submitted())  # Join names into a single string
        print(f"These workers didn't submit shifts: {notSubmitted}.")

        

if __name__ == "__main__":
    main()
