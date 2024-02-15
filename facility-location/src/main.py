from data import generate_random_instance
from master_problem import solve_CFLP

if __name__ == "__main__":
    # Generate a random instance with 100 customers and 10 facilities
    data = generate_random_instance(num_customers=100, num_facilities=10)

    # Solve the Capacitated Facility Location Problem (CFLP) model and obtain the optimal solution
    solution = solve_CFLP(data)

    # Print solution information
    print("Objective value:    ", solution.objective_value)
    print("Open facilities:    ", [j for j in data.J if solution.locations[j] > 0.5])
    print("Solution time (sec):", solution.solution_time)
    print("Number of optimality cuts generated:", solution.num_cuts)
