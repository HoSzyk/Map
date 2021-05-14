from problem import CspProblem


class BaseVariableHeuristic:
    def get_variables(self, problem: CspProblem):
        return problem.variables


class NeighbourHeuristic(BaseVariableHeuristic):
    def get_variables(self, problem: CspProblem):
        return sorted(problem.variables, key=lambda x: len(problem.neighbours[x]), reverse=True)


class DegreeHeuristic(BaseVariableHeuristic):
    def get_variables(self, problem: CspProblem):

        sort_dict = {}

        for constraint in problem.constraints:
            for elem in constraint.elements:
                if elem not in sort_dict:
                    sort_dict[elem] = 0
                else:
                    sort_dict[elem] += 1

        return sorted(problem.variables, key=lambda x: sort_dict[x], reverse=True)
