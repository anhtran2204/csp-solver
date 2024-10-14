import sys

global counter
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

# def most_constrained_variable(domains, constraints):

# def most_constraining_variable(domains, constraints):

# def least_constraining_value(domains, constraints, variable): 

def is_consistent(var, value, assignment, constraints):
    assignment[var] = value
    for constraint in constraints:
        var1, op, var2 = constraint
        if var == var1 or var == var2:
            if var == var1 and var2 in assignment:
                if not evaluate_constraints(var, op, var2, assignment):
                    return False
            elif var == var2 and var1 in assignment:
                if not evaluate_constraints(var1, op, var, assignment):
                    return False
    return True

def evaluate_constraints(var1, op, var2, assignment):
    if op == "<":
        return assignment[var1] < assignment[var2]
    elif op == ">":
        return assignment[var1] > assignment[var2]
    elif op == "=":
        return assignment[var1] == assignment[var2]
    elif op == "!":
        return assignment[var1] != assignment[var2]

# def inferences(assignment, domains, constraints, variable, value):

def backtracking_search(counter, assignment, domains, constraints, procedure=False):
    if len(assignment) == len(domains):
        counter += 1
        # print(assignment, "solution")
        return True
    var = select_unassigned_variable(assignment, domains, constraints)
    for value in order_domain_values(var, domains):
        print(var, value)
        if is_consistent(var, value, assignment, constraints):
            if counter >= 30:
                sys.exit(1)
            if len(domains[var]) == 0:
                # print(assignment, "failure")
                counter += 1
                return False
            assignment[var] = value
            print(assignment)
            result = backtracking_search(counter, assignment, domains, constraints, procedure)
            if result:
                counter += 1
                return True
            assignment.pop(var, None)
    counter += 1
    # print(assignment, "failure")
    return False
            
    # var = most_constrained_variable(domains, constraints)
    # for value in domains[var]:
    #     if value.is_consistent(assignment, constraints):
    #         assignment[var] = value
    #         if procedure:
    #             inference = forward_checking(assignment, var, domains, constraints)
    #             if inference != None:
    #                 assignment.update(inference)
    #             else:
    #                 print(assignment, "failure")
    #         else:
    #             new_domains = domains.copy()
    #         result = recursive_backtracking(assignment, new_domains, constraints, procedure)
    #         if result:
    #             print(assignment, "solution")
    #             return True
    #         assignment.pop(var, None)
    #         assignment.pop(inference, None)
    # return False

# def forward_checking(assignment, var, domains, constraints):
#     temp_domains = domains.copy()
#     for (var1, op, var2) in constraints:
#         if var1 == var and var2 not in assignment:


def csp_solver(varFile, conFile, procedure):
    domains = parse_domains(varFile)
    constraints = parse_constraints(conFile)
    assignment = {}
    counter = 0
    if procedure == "none":
        backtracking_search(counter, assignment, domains, constraints)
    elif procedure == "fc":
        backtracking_search(counter, assignment, domains, constraints, True)

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