from abc import ABC, abstractmethod


class BaseConstraint(ABC):
    def __init__(self, elements):
        self.__elements = elements

    def values(self, solution):
        result = [solution[index] for index in self.__elements]
        return result

    @property
    def elements(self):
        return self.__elements

    @abstractmethod
    def check_constraint(self, solution):
        pass


class FunctionalConstraint(BaseConstraint):
    def __init__(self, elements, func):
        super().__init__(elements)
        self.__func = func

    def check_constraint(self, solution):
        values = self.values(solution)
        return True if None in values else self.__func(*values)


class EqualsElements(BaseConstraint):
    def check_constraint(self, solution):
        values = [elem for elem in self.values(solution) if elem is not None]
        return len(set(values)) <= 1


class DifferentElements(BaseConstraint):
    def check_constraint(self, solution):
        values = [elem for elem in self.values(solution) if elem is not None]
        return len(values) == len(set(values))
