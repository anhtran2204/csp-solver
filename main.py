import sys

counter = 0

def parse_domains(varFile):
    file = open(varFile, "r")
    line = file.readline()

    domains = {}
    while line:
        var, values = line.split(":")
        domains[var.strip()] = list(map(int, values.split()))
        line = file.readline()
    return domains

def parse_constraints(conFile):
    file = open(conFile, "r")
    line = file.readline()

    constraints = []
    while line:
        var1, op, var2 = line.split()
        constraints.append((var1, op, var2))
        line = file.readline()
    return constraints

def select_unassigned_variable(assignment, domains, constraints):
    return next(var for var in domains if var not in assignment)

def order_domain_values(var, domains):
    return sorted(domains[var])

def most_constrained_variable(assignment, domains, constraints):
    # Step 1: Get the list of unassigned variables
    unassigned_vars = []
    for var in domains:
        if var not in assignment:
            unassigned_vars.append(var)

    # Step 2: Find the variable with the smallest domain size
    best_var = None
    best_value = None
    for var in unassigned_vars:
        domain_size = len(domains[var])
        constraining_count = -most_constraining_variable(assignment, var, constraints)  # Inverse for tie-breaking

        # If no best_var has been selected yet, choose the first one
        if best_var is None:
            best_var = var
            best_value = (domain_size, constraining_count, var)

        else:
            # Compare current var with the current best one
            current_value = (domain_size, constraining_count, var)
            if current_value < best_value:
                best_var = var
                best_value = current_value

    return best_var

def most_constraining_variable(assignment, var, constraints):
    num_constraints = 0
    for constraint in constraints:
        var1, op, var2 = constraint
        if var == var1 or var == var2:
            if var == var1 and var2 not in assignment:
                num_constraints += 1
            elif var == var2 and var1 not in assignment:
                num_constraints += 1
    return num_constraints 

def least_constraining_value(var, assignment, domains, constraints): 
    constraining_values = {}
    least_constraining_values = []

    for value in domains[var]:
        possible_values = 0
        for constraint in constraints:
            var1, op, var2 = constraint
            if var == var1 and var2 not in assignment:
                for value2 in domains[var2]:
                    if not evaluate_constraints(assignment, var, op, var2, value, value2):
                        possible_values += 1
            elif var == var2 and var1 not in assignment:
                for value1 in domains[var1]:
                    if not evaluate_constraints(assignment, var1, op, var, value1, value):
                        possible_values += 1

        if possible_values in constraining_values:
            constraining_values[possible_values].append(value)
        else:
            constraining_values[possible_values] = [value]

    for key in sorted(constraining_values.keys()):
        least_constraining_values += constraining_values[key]

    return least_constraining_values

def is_consistent(var, value, assignment, constraints):
    for constraint in constraints:
        var1, op, var2 = constraint
        if var == var1 or var == var2:
            if var == var1 and var2 in assignment:
                if not evaluate_constraints(assignment, var, op, var2, value, assignment[var2]):
                    return False
            elif var == var2 and var1 in assignment:
                if not evaluate_constraints(assignment, var1, op, var, assignment[var1], value):
                    return False
    return True 

def evaluate_constraints(assignment, var1, op, var2,val1=None, val2=None):
    v1 = assignment.get(var1, val1)
    v2 = assignment.get(var2, val2)
    if op == "=":
        return v1 == v2
    elif op == "!":
        return v1 != v2
    elif op == ">":
        return v1 > v2
    elif op == "<":
        return v1 < v2

def print_assignment(counter, assignment, status):
    c = 0
    print(counter, ". ", end="", sep="")
    for v in assignment.keys():
        if c is len(assignment.keys()) - 1:
            print(v, "=", assignment[v], status, sep="")
        else:
            print(v, "=", assignment[v], ", ", end="", sep="")
        c += 1

def backtracking_search(assignment, domains, constraints, procedure=False):
    global counter
    if len(assignment) == len(domains):
        counter += 1
        # print(assignment, "solution")
        print_assignment(counter, assignment, " solution")
        return True
    var = most_constrained_variable(assignment, domains, constraints)
    values = least_constraining_value(var, assignment, domains, constraints)
    for value in values:
        assignment[var] = value
        if is_consistent(var, value, assignment, constraints):
            if len(domains[var]) == 0:
                counter += 1
                # print(assignment, "failure")
                print_assignment(counter, assignment, " failure")
            if procedure:
                new_domains = forward_checking(assignment, var, domains, constraints)
            else:
                new_domains = domains.copy()
            result = backtracking_search(assignment, new_domains, constraints, procedure)
            if result is not False:
                return result
            assignment.pop(var, None)
        else:
            counter += 1
            # print(assignment, "failure")
            print_assignment(counter, assignment, " failure")
            assignment.pop(var, None)
        if counter >= 30:
            sys.exit()
    return False

def forward_checking(assignment, var, domains, constraints):
    local_domains = domains.copy()
    for constraint in constraints:
        var1, op, var2 = constraint
        if var1 == var and var2 not in assignment:
            for value in domains[var2]:
                if not evaluate_constraints(assignment, var, op, var2, value):
                    local_domains[var2].remove(value)
                    if not local_domains[var2]:
                        return None
    return local_domains

def csp_solver(varFile, conFile, procedure):
    domains = parse_domains(varFile)
    constraints = parse_constraints(conFile)
    assignment = {}
    if procedure == "none":
        backtracking_search(assignment, domains, constraints)
    elif procedure == "fc":
        backtracking_search(assignment, domains, constraints, True)

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <varFile> <conFile> <procedure>")
        sys.exit(1)

    varFile = sys.argv[1]
    conFile = sys.argv[2]
    procedure = sys.argv[3]
    csp_solver(varFile, conFile, procedure)

if __name__ == "__main__":
    main()