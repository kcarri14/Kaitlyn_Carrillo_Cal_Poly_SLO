class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # list of variables
        self.domains = domains  # dict of domains for each variable
        self.constraints = constraints  # list of constraints (functions)

    def is_consistent(self, variable, assignment):
        """Check if the current assignment is consistent."""
        for constraint in self.constraints:
            if not constraint(assignment):
                return False
        return True

    def backtrack(self, assignment):
        """Backtrack search to find a solution."""
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.is_consistent(first, local_assignment):
                result = self.backtrack(local_assignment)
                if result is not None:
                    return result
        return None

    def solve(self):
        """Solve the CSP."""
        return self.backtrack({})
 #i didn't wanna mess with the original code given to us so I made a separate function  
    def solve_all(self, max_solutions=None):
        solutions = []
        #same as the other back_tracking put it doesnt stop at the first time it finds a solution
        def back_tracking_all(assignment):
            if len(assignment) == len(self.variables):
                solutions.append(assignment.copy())
                return
            unassigned = [v for v in self.variables if v not in assignment]
            first = unassigned[0]
            for value in self.domains[first]:
                local_assignment = assignment.copy()
                local_assignment[first] = value
                if self.is_consistent(first, local_assignment):
                    back_tracking_all(local_assignment)
                    if max_solutions is not None and len(solutions) >= max_solutions:
                        return

        back_tracking_all({})
        return solutions
    
#builds the coloring from the adjacency list that it is given
def build_map_coloring_csp(adjacency, colors):
    regions = list(adjacency.keys())
    domains = {}
    neighbors = {}
    #puts the colors in a dictionary with each item in the adjacency list
    # and each neighbor goes into a dictionary so that it can be used later
    for r in regions:
        domains[r] = list(colors)
        neighbors[r] = set(adjacency[r])

    for r, nbs in list(neighbors.items()):
        for n in nbs:
            neighbors.setdefault(n, set()).add(r)

    constraints = [(lambda a, n=neighbors: constraint_functions(a, n))]

    return CSP(regions, domains, constraints)

def constraint_functions(assignment, neighbors):
    for r, nbs in neighbors.items():
        if r in assignment:
            for n in nbs:
                if n in assignment and assignment[r] == assignment[n]:
                    return False
    return True

Australia = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "Q"],
    "SA":  ["WA", "NT", "Q", "NSW", "V"],
    "Q":   ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V":   ["SA", "NSW", "T"],
    "T":   ["V"]
}


colors = ["blue", "green", "red"]

# Build CSP
map_csp = build_map_coloring_csp(Australia, colors)

solution = map_csp.solve()
print(solution)

all_solutions = map_csp.solve_all()
for i, sol in enumerate(all_solutions, 1):
    print(f"Solution {i}: {sol}")


    


"""# Example CSP: Sudoku
def sudoku_constraints(assignment):
    #Define constraints for Sudoku.
    for i in range(9):
        row = [assignment.get((i, j)) for j in range(9) if (i, j) in assignment]
        col = [assignment.get((j, i)) for j in range(9) if (j, i) in assignment]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return False
    return True

# Variables and domains for a simple 4x4 Sudoku
variables = [(i, j) for i in range(4) for j in range(4)]
domains = {var: list(range(1, 5)) for var in variables}
constraints = [sudoku_constraints]

# Creating CSP instance
sudoku_csp = CSP(variables, domains, constraints)
solution = sudoku_csp.solve()
print("Sudoku Solution:", solution)"""