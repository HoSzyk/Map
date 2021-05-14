from solvers import backtracking_search, forward_checking, ac3
from map_problem import *
from einstein import *
from random import seed
from variable_heuristic import *
from value_heuristic import *
from time import time_ns


if __name__ == '__main__':
    # seed("1")

    var_heuristic = DegreeHeuristic()
    val_heuristic = LeastConstrainingValueHeuristic()

    # generator = MapGenerator(DEFAULT_SIZE_X, DEFAULT_SIZE_Y, NUMBER_OF_POINTS)
    # edges, points = generator.generate_map()
    # map_problem = MapProblem(edges, NUMBER_OF_COLORS, points, DEFAULT_SIZE_X, DEFAULT_SIZE_Y)
    # print('Map generated')

    # ac3(map_problem)
    #
    # seed("1")
    #
    # start_time = time_ns()
    #
    # solutions = backtracking_search(map_problem, var_heuristic, val_heuristic)
    #
    # print(f'End time back map problem is : {(time_ns() - start_time) * 10 ** (-9)} s - {solutions[1]}')
    #
    # seed("1")
    #
    # start_time = time_ns()
    #
    # solutions = forward_checking(map_problem, var_heuristic, val_heuristic)
    #
    # print(f'End time forward map problem is : {(time_ns() - start_time) * 10 ** (-9)} s - {solutions[1]}')

    # if ac3(map_problem):
    #     solutions = forward_checking(map_problem, var_heuristic, val_heuristic)
    #
    #     print(f'End time map problem is : {(time_ns() - start_time) * 10**(-9)} s - {solutions[1]}')
    #
    #     # if solutions is not None:
    #     #     map_problem.possible_solution = solutions[0][0]
    #     #     map_problem.plot_map()
    #     #
    #     #     print('\n'.join(map(lambda x: str(x), solutions)))
    #     #
    #     # else:
    #     #     dictionary = {i: 0 for i in range(NUMBER_OF_POINTS)}
    #     #     map_problem.possible_solution = dictionary
    #     #     map_problem.plot_map()
    # else:
    #     print('Brak rozwiazan')

    # -----------------------------------------------------------------

    einstein_problem = EinsteinProblem()

    start_time = time_ns()
    ac3(einstein_problem)

    # solution_einstein = forward_checking(einstein_problem, var_heuristic, val_heuristic)
    # print(f'End time einstein is : {(time_ns() - start_time) * 10 ** (-9)} s - {solution_einstein[1]}')

    if ac3(einstein_problem):

        solution_einstein = forward_checking(einstein_problem, var_heuristic, val_heuristic)
        print(f'End time einstein is : {(time_ns() - start_time) * 10**(-9)} s - {solution_einstein[1]}')
        # example_solution = solution_einstein[0][0]
        # result = [[], [], [], [], []]
        #
        # for elem, value in example_solution.items():
        #     result[value - 1].append(elem)
        #
        # print('\n'.join(map(lambda x: str(x), result)))

    print()
