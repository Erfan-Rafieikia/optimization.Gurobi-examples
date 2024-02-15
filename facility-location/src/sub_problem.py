from data import Data
from gurobipy import GRB, Model, quicksum, tupledict


def __set_params(model: Model) -> None:
    """Set the parameters for the Gurobi solver to suppress console output."""
    model.Params.OutputFlag = 0


def solve_subproblem(dat: Data, facility_open: tupledict) -> tuple:
    """
    Solve the subproblem for the Facility Location Problem (FLP).

    This function defines and optimizes the subproblem given the facility open decisions.
    It calculates the optimal shipment quantities from facilities to customers minimizing
    the total shipment costs while satisfying demand and capacity constraints.

    Args:
        data (Data): The input data containing costs, demands, and capacities.
        facility_open (tupledict): A dictionary with facility indices as keys and binary
                                   decisions (1 if open, 0 if closed) as values.

    Returns:
        tuple: A tuple containing the objective value, dual values for demand constraints
               (mu), and dual values for capacity constraints (nu).
    """

    with Model("FLP_Sub") as model:
        __set_params(model)

        # Decision variables for shipment quantities from facilities to customers
        x = model.addVars(dat.I, dat.J, name="x")

        # Objective: Minimize total shipment costs
        total_cost = quicksum(dat.shipment_costs[i, j] * x[i, j] for i in dat.I for j in dat.J)
        model.setObjective(total_cost, GRB.MINIMIZE)

        # Constraints: Satisfy demand for each customer
        demand_constraints = model.addConstrs(
            (quicksum(x[i, j] for j in dat.J) >= dat.demands[i] for i in dat.I),
            name="Demand",
        )

        # Constraints: Do not exceed capacity for open facilities
        capacity_constraints = model.addConstrs(
            (
                quicksum(x[i, j] for i in dat.I) <= dat.capacities[j] * facility_open[j]
                for j in dat.J
            ),
            name="Capacity",
        )

        # Optimize the model to find the best shipment plan
        model.optimize()

        # Retrieve the objective value and dual values from optimized model
        objective_value = model.ObjVal
        mu_values = [demand_constraints[i].Pi for i in dat.I]
        nu_values = [capacity_constraints[j].Pi for j in dat.J]

    return objective_value, mu_values, nu_values
