from dataclasses import dataclass

import numpy as np

SEED = 2024  # random seed for reproducibility

DEMANDS = (1, 101)  # the range of customer demands
CAPACITIES = (500, 1001)  # the range of facility capacities
FIXED_COSTS = (1000, 5001)  # the range of facility fixed costs
SHIPMENT_COSTS = (1, 10)  # the range of shipment costs


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

    demands = np.random.randint(low=DEMANDS[0], high=DEMANDS[1], size=num_customers)
    capacities = np.random.randint(low=CAPACITIES[0], high=CAPACITIES[1], size=num_facilities)
    fixed_costs = np.random.uniform(low=FIXED_COSTS[0], high=FIXED_COSTS[1], size=num_facilities)

    # Create a cost matrix
    shipment_costs = np.random.uniform(
        low=SHIPMENT_COSTS[0], high=SHIPMENT_COSTS[1], size=(num_customers, num_facilities)
    )

    return Data(
        I=I,
        J=J,
        demands=demands,
        capacities=capacities,
        fixed_costs=fixed_costs,
        shipment_costs=shipment_costs,
    )
