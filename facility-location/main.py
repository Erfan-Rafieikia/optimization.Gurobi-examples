from data import generate_random_instance
from master_problem import solve_CFLP

if __name__ == "__main__":
    # generate a random instance
    data = generate_random_instance(num_customers=100, num_facilities=10)
    # solve the CFLP model and get the optimal solution
    obj, y_values = solve_CFLP(data)

    print("Objective value: ", obj)
    print("Open facilities: ", [j for j in data.J if y_values[j] > 0.5])
