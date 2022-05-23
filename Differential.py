from math import floor
import random
from re import I
from secrets import choice
from types import new_class
from typing import List
from Coord import Coord
from Map import Map
from Individual import Individual
from Individual import calc_distance

DIMENSIONS = 2


class DifferentialEvolution:
    def __init__(self, map: Map, step_size=0.7, crossover_rate=0.3) -> None:
        self.map = map
        self.step_size = step_size
        self.crossover_rate = crossover_rate
        self.objective = map.get_goal_coords()
        self.population: List[Individual] = []

    def initial_population(self, population_length: int):
        starting_coords = self.map.get_starting_coords()
        new_population = []
        for _ in range(population_length):
            new_population.append(Individual(choice(starting_coords)))
        self.population = new_population

    def get_best_solution(self):
        best = self.population[0]
        best_dist = self.population[0].distance_to(self.objective)
        for indv in self.population:
            dist = indv.distance_to(self.objective)
            if best_dist > dist:
                best = indv
                best_dist = dist
        return best

    def __random_index(self):
        return random.randint(0, len(self.population)-1)

    def __get_mutant_vector(self,  index) -> Coord:
        r1 = self.__random_index()
        while r1 == index:
            r1 = self.__random_index()
        r2 = self.__random_index()
        while r2 == index or r2 == r1:
            r2 = self.__random_index()
        r3 = self.__random_index()
        while r3 == index or r3 == r1 or r3 == r2:
            r3 = self.__random_index()
        r2_position = self.population[r2].get_position()
        r3_position = self.population[r3].get_position()
        x_distance = r2_position.X - r3_position.X
        y_distance = r2_position.Y - r3_position.Y

        original_indv = self.population[r1]
        original_pos = original_indv.get_position()
        new_pos = Coord(floor(original_pos.X+x_distance*self.step_size),
                        floor(original_pos.Y+y_distance*self.step_size))
        if (not self.map.is_position_valid(new_pos)):
            return None
        return new_pos

    def __get_test_vector(self, original_indv: Individual, mutant: Coord):
        Jr = random.randint(0, DIMENSIONS-1)
        original_pos = original_indv.get_position()
        test_vector = Individual(original_pos, original_indv.get_history())
        dimensions = [original_pos.X, original_pos.Y]
        mutant_dimensions = [mutant.X, mutant.Y]
        for d in range(len(dimensions)):
            r = random.uniform(0, 1)
            if r < self.crossover_rate or d == Jr:
                dimensions[d] = mutant_dimensions[d]
        new_pos = Coord(dimensions[0], dimensions[1])
        if not self.map.is_position_valid(new_pos):
            return None
        test_vector.set_position(new_pos)
        return test_vector

    def epoch(self):
        test_vectors: List[Individual] = []

        for index, indv in enumerate(self.population):
            mutant = self.__get_mutant_vector(index)
            while mutant == None:
                mutant = self.__get_mutant_vector(index)
            test_vector = self.__get_test_vector(indv, mutant)
            while test_vector == None:
                test_vector = self.__get_test_vector(indv, mutant)
            test_vectors.append(test_vector)

        for index in range(len(self.population)):
            if test_vectors[index].distance_to(self.objective) < self.population[index].distance_to(self.objective):
                self.population[index] = test_vectors[index]

    def run(self, population=20, max_steps=200, tolerance=4):
        self.initial_population(population)
        generations = 0
        best_sol = self.get_best_solution()
        while best_sol.distance_to(self.objective) > tolerance and generations < max_steps:
            best_sol = self.get_best_solution()
            generations += 1
            self.epoch()
        return self.get_best_solution()
