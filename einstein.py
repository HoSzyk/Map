from problem import CspProblem
from constraint import EqualsElements, DifferentElements, FunctionalConstraint

from constants import nationalities, colors, cigarettes, animals, drinks


class EinsteinProblem(CspProblem):
    def __init__(self):
        self.__variables = []
        self.__domains = {}
        self.__constraints = []
        self.init_problem()
        self.__neighbours = self.initialize_neighbours()
        self.__variable_specific_constraint = self.initialize_variable_specific_constraint()

    @property
    def variables(self):
        return self.__variables

    @property
    def domains(self):
        return self.__domains

    @property
    def constraints(self):
        return self.__constraints

    @property
    def neighbours(self):
        return self.__neighbours

    @property
    def variable_specific_constraint(self):
        return self.__variable_specific_constraint

    def init_problem(self):
        self.__variables = [e for elem in (nationalities, colors, cigarettes, drinks, animals) for e in elem]
        self.__domains = {element: list(range(1, 6)) for element in self.__variables}
        new_constraints = [
                DifferentElements(elem) for elem in (nationalities, colors, cigarettes, drinks, animals)    # Different
            ] + \
            [
                FunctionalConstraint(['Norweg'], lambda elem: elem == 1),  # C1
                EqualsElements(['Anglik', 'Czerwony']),  # C2
                FunctionalConstraint(['Bialy', 'Zielony'], lambda elem1, elem2: elem1 - elem2 == 1),  # C3
                EqualsElements(['Dunczyk', 'Herbata']),  # C4
                FunctionalConstraint(['Light', 'Koty'], lambda elem1, elem2: abs(elem1 - elem2) == 1),  # C5
                EqualsElements(['Zolty', 'Cygaro']),  # C6
                EqualsElements(['Niemiec', 'Fajka']),  # C7
                FunctionalConstraint(['Mleko'], lambda elem: elem == 3),  # C8
                FunctionalConstraint(['Light', 'Woda'], lambda elem1, elem2: abs(elem1 - elem2) == 1),  # C9
                EqualsElements(['PapierosBF', 'Ptaki']),  # C10
                EqualsElements(['Szwed', 'Psy']),  # C11
                FunctionalConstraint(['Norweg', 'Niebieski'], lambda elem1, elem2: abs(elem1 - elem2) == 1),  # C12
                FunctionalConstraint(['Konie', 'Zolty'], lambda elem1, elem2: abs(elem1 - elem2) == 1),  # C13
                EqualsElements(['Mentolowe', 'Piwo']),  # C14
                EqualsElements(['Zielony', 'Kawa'])  # C15
            ]
        self.__constraints = new_constraints
