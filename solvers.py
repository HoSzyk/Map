from copy import deepcopy

from value_heuristic import *
from variable_heuristic import *
from constants import SINGLE_SOLUTION


def backtracking_search(problem: CspProblem,
                        variable_heuristic: BaseVariableHeuristic,
                        value_heuristic: BaseValueHeuristic):
    initial_solution = dict.fromkeys(problem.variables)
    unassigned_variables = variable_heuristic.get_variables(problem)

    solutions = recursive_backtracking(problem, initial_solution, unassigned_variables, value_heuristic)
    return solutions


def recursive_backtracking(problem: CspProblem, assignment, unassigned_variables, value_heuristic: BaseValueHeuristic):
    results = []
    visited = 0

    if len(unassigned_variables) == 0:
        return [assignment], visited

    # Getting variable

    var = unassigned_variables[0]
    local_unassigned_var = deepcopy(unassigned_variables[1:])

    # Choosing value

    values = value_heuristic.get_values(problem, assignment, problem.domains, var)

    for value in values:
        local_assignment = assignment.copy()
        local_assignment[var] = value

        visited += 1

        if problem.is_correct_solution(local_assignment):
            result, temp = recursive_backtracking(problem, local_assignment, local_unassigned_var, value_heuristic)
            visited += temp
            if result is not None:
                if SINGLE_SOLUTION:
                    return result, visited
                results.extend(result)

    if results is not None and len(results) != 0:
        return results, visited
    else:
        return None, visited


def forward_checking(problem: CspProblem,
                     variable_heuristic: BaseVariableHeuristic,
                     value_heuristic: BaseValueHeuristic):
    initial_solution = dict.fromkeys(problem.variables)
    unassigned_variables = variable_heuristic.get_variables(problem)
    result = forward_helper(problem, problem.domains, initial_solution, unassigned_variables, value_heuristic)

    return result


def forward_helper(problem: CspProblem, domains, assignment, unassigned_variables, value_heuristic: BaseValueHeuristic):
    results = []
    visited = 0

    if len(unassigned_variables) == 0:
        return [assignment], visited

    var = unassigned_variables[0]
    local_unassigned_var = deepcopy(unassigned_variables[1:])

    values = value_heuristic.get_values(problem, assignment, domains, var)

    for value in values:
        local_assignment = assignment.copy()
        local_domains = deepcopy(domains)
        local_assignment[var] = value
        local_domains[var] = [value]

        visited += 1

        # Remove inconsistent from domains
        for neighbour in problem.neighbours[var]:
            if local_assignment[neighbour] is None:
                inconsistent = []
                for neighbour_value in local_domains[neighbour]:
                    local_assignment[neighbour] = neighbour_value
                    if not problem.is_correct_for(local_assignment, neighbour):
                        inconsistent.append(neighbour_value)
                    local_assignment[neighbour] = None
                for elem in inconsistent:
                    local_domains[neighbour].remove(elem)

        flag = True

        for variable in local_unassigned_var:
            if len(local_domains[variable]) == 0:
                flag = False

        if flag:
            if problem.is_correct_solution(local_assignment):
                result, temp = forward_helper(problem,
                                              local_domains,
                                              local_assignment,
                                              local_unassigned_var,
                                              value_heuristic)
                visited += temp
                if result is not None:
                    if SINGLE_SOLUTION:
                        return result, visited
                    results.extend(result)

    if results is not None and len(results) != 0:
        return results, visited
    else:
        return None, visited


def ac3(problem: CspProblem):
    assigment = dict.fromkeys(problem.variables)
    queue = []

    for constraint in problem.constraints:
        if len(constraint.elements) == 1:
            variable = constraint.elements[0]
            for value in problem.domains[variable]:
                assigment[variable] = value
                if not problem.is_correct_for(assigment, variable):
                    problem.domains[variable].remove(value)
                assigment[variable] = None
        else:
            queue.extend([(constraint.elements[i], constraint.elements[j])
                          for i in range(len(constraint.elements))
                          for j in range(len(constraint.elements))
                          if i != j])

    while len(queue) > 0:
        arc = queue[0]
        queue = queue[1:]
        if arc_reduce(problem, arc[0], arc[1]):
            if len(problem.domains[arc[0]]) == 0:
                return False
            else:
                queue.extend([(arc[0], neighbour)
                              for neighbour in problem.neighbours[arc[0]]])
    return True


def arc_reduce(problem: CspProblem, x, y):
    temp_assignment = dict.fromkeys(problem.variables)
    change = False
    inconsistent = []
    for x_value in problem.domains[x]:
        temp_assignment[x] = x_value
        exist_correct = False
        for y_value in problem.domains[y]:
            temp_assignment[y] = y_value
            if problem.is_correct_for(temp_assignment, x):
                exist_correct = True
        if not exist_correct:
            inconsistent.append(x_value)
    for elem in inconsistent:
        problem.domains[x].remove(elem)
        change = True
    return change
