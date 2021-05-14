from random import shuffle
from problem import CspProblem


class BaseValueHeuristic:
    def get_values(self, problem: CspProblem, assigment, domains, variable):
        return domains[variable]


class LeastConstrainingValueHeuristic(BaseValueHeuristic):
    def get_values(self, problem: CspProblem, assigment, domains, variable):

        if len(domains[variable]) == 1:
            return domains[variable]

        conflicts = []

        for value in domains[variable]:
            acc = 0

            assigment[variable] = value
            for neighbour in problem.neighbours[variable]:
                if assigment[neighbour] is None:
                    for neighbour_value in domains[neighbour]:
                        assigment[neighbour] = neighbour_value
                        if not problem.is_correct_for(assigment, variable):
                            acc += 1
                        assigment[neighbour] = None
            conflicts.append(acc)

        assigment[variable] = None

        return [
            val
            for _, val in sorted(
                zip(conflicts, domains[variable]), key=lambda x: x[0]
            )
        ]


class RandomValueHeuristic(BaseValueHeuristic):
    def get_values(self, problem: CspProblem, assigment, domains, variable):
        return shuffle(domains[variable])
