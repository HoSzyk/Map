from abc import ABC, abstractmethod


class CspProblem(ABC):

    @property
    @abstractmethod
    def variables(self):
        pass

    @property
    @abstractmethod
    def domains(self):
        pass

    @property
    @abstractmethod
    def constraints(self):
        pass

    @property
    @abstractmethod
    def neighbours(self):
        pass

    @property
    @abstractmethod
    def variable_specific_constraint(self):
        pass

    def is_correct_solution(self, solution):
        for constraint in self.constraints:
            if not constraint.check_constraint(solution):
                return False
        return True

    def initialize_neighbours(self):
        result = {}

        for constraint in self.constraints:
            for elem in constraint.elements:
                if elem not in result:
                    result[elem] = set(constraint.elements)
                else:
                    result[elem].update(constraint.elements)

        for key in result:
            result[key].remove(key)

        return result

    def initialize_variable_specific_constraint(self):
        return {
            variable: [
                const
                for const in self.constraints
                if variable in const.elements
            ]
            for variable in self.variables
        }

    def is_correct_for(self, solution, variable):
        for const in self.variable_specific_constraint[variable]:
            if not const.check_constraint(solution):
                return False
        return True
