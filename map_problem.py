from problem import CspProblem
from constraint import DifferentElements
from shapely.geometry import Point, LineString
from typing import Dict, List
from random import randint, sample
import matplotlib.pyplot as plt
from constants import *


class MapProblem(CspProblem):
    def __init__(self, edges, num_colors, points, size_x, size_y):
        self.__edges = edges
        self.__points = points
        self.__size_x = size_x
        self.__size_y = size_y
        self.__variables = list(edges.keys())

        self.__domains = {element: list(range(num_colors)) for element in self.__variables}
        self.__solution = {}
        connections = []
        for start_point in edges:
            for end_point in edges[start_point]:
                if not (end_point, start_point) in connections:
                    connections.append((start_point, end_point))

        self.__constraints = [DifferentElements(elements) for elements in connections]
        self.__neighbours = self.initialize_neighbours()
        self.__variable_specific_constraint = self.initialize_variable_specific_constraint()

    @property
    def problem_edges(self):
        return self.__edges

    @problem_edges.setter
    def problem_edges(self, edges):
        self.__edges = edges

    @property
    def possible_solution(self):
        return self.__solution

    @possible_solution.setter
    def possible_solution(self, possible_solution):
        self.__solution = possible_solution

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

    def plot_map(self):
        if self.__solution is not None:
            list_x = []
            list_y = []
            plt.grid()
            plt.axis([-1, self.__size_x, -1, self.__size_y])
            plt.xticks(range(self.__size_x + 1))
            plt.yticks(range(self.__size_y + 1))
            for point in self.__points.values():
                list_x.append(point.x)
                list_y.append(point.y)

            for key, elem in self.__edges.items():
                for edge in elem:
                    self.__draw_connection(list_x, list_y, key, edge)
            plt.show()

    def __draw_connection(self, x, y, p1, p2, color='#737373'):
        if self.__solution[p1] is not None:
            color = DEFAULT_COLORS[self.__solution[p1]]

        x1, x2 = x[p1], x[p2]
        y1, y2 = y[p1], y[p2]
        plt.scatter([x1], [y1], c=color)
        plt.plot([x1, x2], [y1, y2], 'k-')


class MapGenerator:
    def __init__(self, size_x, size_y, num_points):
        self.__size_x = size_x
        self.__size_y = size_y
        self.__num_points = num_points

    @staticmethod
    def add_new(start: int, end: int, connections: List[LineString], points: Dict, edges):
        added = True
        new_line_string = LineString([points[start], points[end]])

        points_local = list(points.values())
        points_local.remove(points[start])
        points_local.remove(points[end])

        for elem in points_local:
            if new_line_string.intersects(elem):
                added = False
                break

        if added:
            for line in connections:
                if not line.touches(new_line_string) and line.intersects(new_line_string):
                    added = False
                    break
        if added:
            connections.append(new_line_string)
            edges[end].append(start)
            edges[start].append(end)
        return added

    def generate_map(self):
        points = []
        line_strings = []
        matrix = {}

        while self.__num_points != len(points):
            x = randint(0, self.__size_x - 1)
            y = randint(0, self.__size_y - 1)
            if (x, y) not in matrix:
                matrix[(x, y)] = 1
                points.append(Point(x, y))

        points = {i: point for i, point in enumerate(points)}
        edges = {i: [] for i in range(len(points))}
        temp_points = points.keys()

        counter = 0
        while counter < NUMBER_OF_ITERATIONS:
            # Get random start and end point
            start, end = sample(temp_points, 2)
            if self.add_new(start, end, line_strings, points, edges):
                counter = 0
            counter += 1
        # Missing lines
        for elem in points:
            end_list = list(points.keys())
            end_list.pop(elem)
            for end in end_list:
                self.add_new(elem, end, line_strings, points, edges)
        return edges, points
