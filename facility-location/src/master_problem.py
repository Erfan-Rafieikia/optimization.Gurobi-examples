from callbacks import Callback
from gurobipy import Model, GRB, quicksum

from data import Data


def __set_params(mod: Model):
    """
    Set the parameters of the Gurobi solver.

    Args:
        mod (Model): The Gurobi model for which the parameters are being set.
    """

    # Turn on lazy constraints adaptation (for optimality cuts)
    mod.Params.LazyConstraints = 1


def solve_CFLP(dat: Data) -> tuple:
    """
    Creates and solves the master problem for the capacitated facility location problem.

    Args:
        dat (Data): The input data for the problem.

    Returns:
        tuple: A tuple containing the objective value and the optimal solution.
    """

    # Create a Gurobi model for the master problem
    with Model("FLP_Master") as mod:
        # set Gurobi parameters
        __set_params(mod)

        # create decision variables
        y = mod.addVars(dat.J, vtype=GRB.BINARY, name="y")
        eta = mod.addVar(name="eta")

        # set the objective function
        # $\min \sum_{j \in J} f_j y_j + \eta$
        expr = quicksum(dat.fixed_costs[j] * y[j] for j in dat.J) + eta
        mod.setObjective(expr, sense=GRB.MINIMIZE)

        # add feasibility constraint
        # allocate enough capacity to meet all demands
        # $\sum_{j \in J} u_j y_j \leq \sum_{i \in I} d_i$
        mod.addConstr(
            (quicksum(dat.capacities[j] * y[j] for j in dat.J) >= dat.demands.sum()),
            name="Feasibility",
        )

        # create callback object
        callback = Callback(dat, y, eta)

        # Write the model
        # mod.write("mp.lp")

        # solve the model using the callback
        mod.optimize(callback)

        # get the objective value
        obj = mod.ObjVal

        # get the optimal solution
        y_values = [y[j].X for j in dat.J]

    return (obj, y_values)
