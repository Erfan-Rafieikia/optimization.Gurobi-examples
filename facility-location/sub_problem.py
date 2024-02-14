from gurobipy import GRB, Model, quicksum

from data import Data


def __set_params(mod: Model):
    """
    Set the parameters of the Gurobi solver.

    Args:
        mod (Model): The Gurobi model for which the parameters are being set.

    Returns:
        None
    """

    mod.Params.OutputFlag = 0  # turn off output


def solve_subproblem(dat: Data, y_value) -> tuple:
    with Model("FLP_Sub") as mod:
        # set Gurobi parameters
        __set_params(mod)

        # create decision variables
        # $x_{ij}$ is the amount of goods shipped from facility $j$ to customer $i$
        x = mod.addVars(dat.I, dat.J, name="x")

        # set the objective function
        # $\min \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}$
        expr = quicksum(dat.shipment_costs[i, j] * x[i, j] for i in dat.I for j in dat.J)
        mod.setObjective(expr, GRB.MINIMIZE)

        # Add constraints
        # demand satisfaction
        # $\sum_{j \in J} x_{ij} \geq d_i$ for all $i \in I$
        demand_constraints = mod.addConstrs(
            (quicksum(x[i, j] for j in dat.J) >= dat.demands[i] for i in dat.I),
            name="Demand",
        )

        # capacity limit
        # $\sum_{i \in I} x_{ij} \leq u_j y_j$ for all $j \in J$
        capacity_constraints = mod.addConstrs(
            (quicksum(x[i, j] for i in dat.I) <= dat.capacities[j] * y_value[j] for j in dat.J),
            name="Capacity",
        )

        # Write the model
        # mod.write("sp.lp")

        # solve the model
        mod.optimize()

        # get the objective value
        obj = mod.ObjVal

        # retrieve dual values
        mu = [demand_constraints[i].Pi for i in dat.I]
        nu = [capacity_constraints[j].Pi for j in dat.J]

    return (obj, mu, nu)
