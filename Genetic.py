from copy import copy
import functools
from math import ceil
import random
from secrets import choice
from typing import List, Tuple
from Coord import Coord
from Individual import Individual
from Map import Map

random.seed(69)


class GeneticAlgothm:
    def __init__(self,  map: Map, mutation_rate=1) -> None:
        self.population: List[Individual] = []
        self.objective = map.get_goal_coords()
        self.mutation_rate = mutation_rate
        self.map = map

    def initial_population(self, population_length: int):
        starting_coords = self.map.get_starting_coords()
        new_population = []
        for _ in range(population_length):
            new_population.append(Individual(choice(starting_coords)))
        self.population = new_population

    def select_couple(self, evaluation_sum):
        tolerance = 10
        while tolerance > 0:
            r = random.uniform(0, 1)
            parent_a = None
            parent_b = None
            for parent in self.population:
                parent_prob = (
                    1/(1+parent.distance_to(self.objective))) / evaluation_sum

                if parent_prob >= r:

                    if parent_a == None:
                        parent_a = parent
                        r = random.uniform(0, 1)
                        while r > parent_prob:
                            r = random.uniform(0, 1)
                        continue

                    if parent_b == None:
                        parent_b = parent
                        r = random.uniform(0, 1)
                        while r > parent_prob:
                            r = random.uniform(0, 1)

                if parent_b != None and parent_a != None:
                    return (parent_a, parent_b)

        if parent_b == None or parent_a == None:
            raise Exception(
                "No hay suficiente material genético. Se están creando clones!!")

    def select_parents(self):
        self.population.sort(key=lambda indv: indv.distance_to(
            self.objective))
        total = functools.reduce(lambda res, indv: res + 1/(1+indv.distance_to(
            self.objective)), self.population, 0)
        couples = []
        for _ in range(ceil(len(self.population)/2)):
            couples.append(self.select_couple(total))
        return couples

    def combine(self, couples: List[Tuple[Individual, Individual]]):
        children = []
        for couple in couples:
            parent_a, parent_b = couple
            parent_a_pos = parent_a.get_position()
            parent_b_pos = parent_b.get_position()

            child_a = Individual(parent_a.get_position(),
                                 parent_a.get_history())
            child_a.set_position(Coord(parent_a_pos.X, parent_b_pos.Y))
            children.append(child_a)

            child_b = Individual(parent_b.get_position(),
                                 parent_b.get_history())
            child_b.set_position(Coord(parent_b_pos.X, parent_a_pos.Y))
            children.append(child_b)
        return children

    def mutate(self, children: List[Individual]):
        mutated = copy(children)
        for child in mutated:
            r = random.uniform(0, 1)
            if r < self.mutation_rate:
                next_pos = choice(
                    self.map.get_possible_movements(child.get_position()))
                child.set_position(next_pos)

        return mutated

    def epoch(self):
        parents = self.select_parents()
        children = self.combine(parents)
        children = self.mutate(children)
        self.population = children

    def run(self, population=20,  max_steps=100000, tolerance=4):
        self.initial_population(population)
        best_sol = self.population[0]
        while best_sol.distance_to(self.objective) > tolerance and len(best_sol.get_history()) < max_steps:
            self.epoch()
            best_sol = self.population[0]
        return best_sol
