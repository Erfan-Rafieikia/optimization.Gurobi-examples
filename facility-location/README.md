# Capacitated Facility Location Problem

This repository provides a Python implementation of the Benders decomposition method for solving the Capacitated Facility Location Problem (CFLP) using the powerful Gurobi solver. The code is designed to be clear, modular, and easily adaptable to specific problem instances.

## CFLP Overview:

The Capacitated Facility Location Problem (CFLP) is a classic optimization problem that involves locating facilities and assigning customers to them, taking into account the capacity limitations of each facility. The objective is to minimize the total cost, which includes both fixed costs for opening facilities and variable costs for serving customers.

### Mathematical Formulation:

The CFLP can be formulated as a mixed-integer linear program (MIP) with the following notations:

#### Sets and Parameters:

- $I$: Set of customers.
- $J$: Set of candidate facility locations.
- $f_{j}$: Fixed cost of opening a facility at location $j \in J$.
- $c_{ij}$: Unit transportation cost between facility $j \in J$ and customer $i \in I$.
- $d_{i}$: Demand of customer $i \in I$.
- $u_{j}$: Capacity of facility $j \in J$.

#### Decision Variables:

- $x_{ij}$: Amount of customer $i$'s demand served by facility $j$.
- $y_{j}$: Binary variable indicating whether facility $j$ is opened (1) or closed (0).

#### Objective Function:

The objective is to minimize the total cost, which includes both fixed costs for opening facilities and variable costs for serving customers:

$$\min\ \sum_{j \in J} f_{j}\, y_{j} + \sum_{i \in I} \sum_{j \in J} c_{ij}\, x_{ij}$$

#### Constraints:

- Demand satisfaction constraint: Each customer's demand must be fully served. 

$$ \sum_{j \in J} x_{ij} \geq d_{i},\ \forall i \in I$$

- Capacity constraint: If a facility is open, the total supply from that facility should not exceed its capacity. If a facility is closed, no supply should be made. 

$$ \sum_{i \in I} x_{ij} \leq u_{j}\, y_{j},\ \forall j \in J$$

- Variable domains:

$$x \in \mathbb{R}^{I \times J}_+,\ y \in \{0, 1\}^{J}$$

### Benders Decomposition Approach

This method effectively tackles large-scale CFLPs by decomposing them into smaller, more manageable subproblems. It operates through two main components: the master problem and the subproblem. These problems interact iteratively until the lower bounds converge to the true optimal solution.
