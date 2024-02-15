from dataclasses import dataclass

from callbacks import Callback
from data import Data
from gurobipy import GRB, Model, quicksum


@dataclass
class Solution:
    objective_value: float
    locations: list
    solution_time: float
    num_cuts: int


def __set_params(mod: Model):
    """
    Set the parameters of the Gurobi solver.

    Args:
        mod (Model): The Gurobi model for which the parameters are being set.
    """

    # Enable lazy constraint adaptation for optimality cuts
    mod.Params.LazyConstraints = 1

    # Use the following to set a time limit for the solver
    # mod.Params.TimeLimit = 60.0


def solve_CFLP(dat: Data, write_mp_lp=False) -> Solution:
    """
    Creates and solves the master problem for the capacitated facility location problem.

    Args:
        dat (Data): The input data for the problem.
        write_mp_lp (bool, optional): Whether to write the model of the initial master problem to an LP file. Defaults to False.

    Returns:
        Solution: An object containing the objective value, optimal locations, solution time, and number of cuts.
    """

    # Create a Gurobi model for the master problem
    with Model("FLP_Master") as mod:
        # Set Gurobi parameters
        __set_params(mod)

        # Create decision variables
        y = mod.addVars(dat.J, vtype=GRB.BINARY, name="y")
        eta = mod.addVar(name="eta")

        # Set the objective function: minimize the sum of fixed costs and eta
        expr = quicksum(dat.fixed_costs[j] * y[j] for j in dat.J) + eta
        mod.setObjective(expr, sense=GRB.MINIMIZE)

        # Add feasibility constraint: allocate enough capacity to meet all demands
        mod.addConstr(
            (quicksum(dat.capacities[j] * y[j] for j in dat.J) >= dat.demands.sum()),
            name="Feasibility",
        )

        # Create callback object
        callback = Callback(dat, y, eta)

        # Write the model to an LP file if specified
        if write_mp_lp:
            mod.write("mp.lp")

        # Solve the model using the callback
        mod.optimize(callback)

        # Get the objective value
        obj = mod.ObjVal

        # Get the solution time
        sol_time = round(mod.Runtime, 2)

        # Get the optimal solution
        y_values = [y[j].X for j in dat.J]

        # Get the number of cuts
        num_cuts = callback.num_cuts

    return Solution(obj, y_values, sol_time, num_cuts)
