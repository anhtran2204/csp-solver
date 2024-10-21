import sys

class CSP:
    def __init__(self, var_file, con_file):
        self.variables = self.parse_var_file(var_file)
        self.constraints = self.parse_con_file(con_file)
        self.assignment = {}
        self.domains = self.variables.copy()  # Copy of the variable domains for forward checking

    def parse_var_file(self, filename):
        variables = {}
        with open(filename) as f:
            for line in f:
                var, values = line.split(":")
                variables[var.strip()] = list(map(int, values.split()))
        return variables

    def parse_con_file(self, filename):
        constraints = []
        with open(filename) as f:
            for line in f:
                var1, op, var2 = line.split()
                constraints.append((var1, op, var2))
        return constraints

    def is_consistent(self, var, value):
        # Check all constraints for this variable
        for (var1, op, var2) in self.constraints:
            if var1 == var or var2 == var:
                if var1 in self.assignment and var2 in self.assignment:
                    if not self.evaluate_constraint(var1, var2, op):
                        return False
                elif var1 == var and var2 in self.assignment:
                    if not self.evaluate_constraint(var, var2, op, value, self.assignment[var2]):
                        return False
                elif var2 == var and var1 in self.assignment:
                    if not self.evaluate_constraint(var1, var, op, self.assignment[var1], value):
                        return False
        return True

    def evaluate_constraint(self, var1, var2, op, val1=None, val2=None):
        v1 = self.assignment.get(var1, val1)
        v2 = self.assignment.get(var2, val2)
        if op == "=":
            return v1 == v2
        elif op == "!":
            return v1 != v2
        elif op == ">":
            return v1 > v2
        elif op == "<":
            return v1 < v2

    def forward_check(self, var, value):
        # Forward checking: Update domains of neighbors
        local_domains = self.domains.copy()
        for (var1, op, var2) in self.constraints:
            if var1 == var and var2 not in self.assignment:
                for v in self.domains[var2]:
                    if not self.evaluate_constraint(var, var2, op, value, v):
                        local_domains[var2].remove(v)
                        if not local_domains[var2]:  # Empty domain, failure
                            return None
        return local_domains

    def backtracking_search(self, forward_checking=False):
        if len(self.assignment) == len(self.variables):
            print(self.assignment, "solution")
            return True

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            self.assignment[var] = value
            if self.is_consistent(var, value):
                local_domains = self.forward_check(var, value) if forward_checking else self.domains
                if forward_checking and local_domains is None:
                    print(self.assignment, "failure")
                else:
                    result = self.backtracking_search(forward_checking)
                    if result:
                        return True
            del self.assignment[var]  # Backtrack
        print(self.assignment, "failure")
        return False

    def select_unassigned_variable(self):
        # Most constrained variable heuristic (minimum domain size)
        unassigned = [v for v in self.variables if v not in self.assignment]
        return min(unassigned, key=lambda var: (len(self.domains[var]), -self.constraining_count(var), var))

    def constraining_count(self, var):
        # Most constraining variable heuristic (number of constraints involving var)
        return sum(1 for (v1, _, v2) in self.constraints if v1 == var or v2 == var)

    def order_domain_values(self, var):
        # Least constraining value heuristic
        return sorted(self.domains[var], key=lambda val: self.constraining_value_count(var, val))

    def constraining_value_count(self, var, value):
        # Count how many constraints a value would affect
        count = 0
        for (var1, op, var2) in self.constraints:
            if var1 == var and var2 not in self.assignment:
                for v in self.domains[var2]:
                    if not self.evaluate_constraint(var, var2, op, value, v):
                        count += 1
        return count

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <var_file> <con_file> <consistency>")
        sys.exit(1)

    var_file = sys.argv[1]
    con_file = sys.argv[2]
    consistency = sys.argv[3]

    csp = CSP(var_file, con_file)

    if consistency == "fc":
        csp.backtracking_search(forward_checking=True)
    else:
        csp.backtracking_search(forward_checking=False)