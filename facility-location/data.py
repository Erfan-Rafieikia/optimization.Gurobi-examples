from dataclasses import dataclass

import numpy as np

SEED = 2024  # random seed for reproducibility


@dataclass
class Data:
    I: np.ndarray  # customer index list
    J: np.ndarray  # facility index list
    demands: np.ndarray
    capacities: np.ndarray
    fixed_costs: np.ndarray
    shipment_costs: np.ndarray


def generate_random_instance(num_customers, num_facilities):
    """
    Generate a random instance for the capacitated facility location problem.

    Args:
        num_customers (int): Number of customers
        num_facilities (int): Number of facilities

    Returns:
        Data: A Data object containing the instance information.
    """

    np.random.seed(SEED)

    I = np.arange(num_customers)
    J = np.arange(num_facilities)

    demands = np.random.randint(low=1, high=101, size=num_customers)
    capacities = np.random.randint(low=500, high=1001, size=num_facilities)
    fixed_costs = np.random.randint(low=1000, high=5001, size=num_facilities)

    # Create a cost matrix
    shipment_costs = np.random.uniform(low=1, high=10, size=(num_customers, num_facilities))

    return Data(
        I=I,
        J=J,
        demands=demands,
        capacities=capacities,
        fixed_costs=fixed_costs,
        shipment_costs=shipment_costs,
    )
