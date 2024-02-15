from data import Data
from gurobipy import GRB, quicksum
from sub_problem import solve_subproblem


class Callback:
    """
    Callback class implementing Benders optimality cuts for the CFLP.  At MIPSOL
    callbacks, solutions are evaluated and lazy optimality cuts are added if needed.
    """

    def __init__(self, dat: Data, y, eta):
        self.dat = dat
        self.y = y
        self.eta = eta

        self.num_cuts = 0  # number of optimality cuts added

    def __call__(self, mod, where):
        """
        Callback entry point: call lazy constraints routine when new
        solutions are found.

        Args:
            mod (Model): The Gurobi model object.
            where (int): The callback event code.

        Returns:
            None
        """
        # check whether an integer feasible solution has been found
        if where == GRB.Callback.MIPSOL:
            # get the current solution
            y_values = mod.cbGetSolution(self.y)
            eta_value = mod.cbGetSolution(self.eta)

            # solve the subproblem and get its dual information
            obj, mu, nu = solve_subproblem(self.dat, y_values)

            # add an optimality cut if needed
            if obj > eta_value:
                self.add_optimality_cut(mod, mu, nu)
                self.num_cuts += 1

    def add_optimality_cut(self, mod, mu, nu):
        """
        Add an optimality cut to the given model.

        Args:
            mod: The model to which the cut is added
            mu: The dual variable values for the demands constraint
            nu: The dual variable values for the capacities constraint

        Returns:
            None
        """

        lhs = quicksum(self.dat.capacities[j] * nu[j] * self.y[j] for j in self.dat.J) + self.eta
        rhs = sum(self.dat.demands[i] * mu[i] for i in self.dat.I)

        # ads the optimality cut as a lazy constraint
        mod.cbLazy(lhs >= rhs)
