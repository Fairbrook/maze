from cmath import cos, sin
from copy import copy, deepcopy
from random import randint, random, uniform
from secrets import choice
from tkinter.messagebox import NO
from turtle import distance
from typing import List, Tuple
from Coord import Coord
from Individual import Individual, calc_distance
from Map import Map
from Vector import Vector
def mul(a, b): return a*b
def sub(a, b): return a-b
def add(a, b): return a+b


Trr = 0.7
k = 0.01
p = 0.9


class Particle(Individual):
    def __init__(self, position=Coord(), history: List[Coord] = [], velocity=Vector(), goal=Coord()) -> None:
        Individual.__init__(self, position, history)
        self.velocity = velocity
        self.best_position = position
        self.theta = 45
        self.dc = 0
        self.temp = 1
        self.best_eval = calc_distance(position, goal)


class Swarm:
    def __init__(self, map: Map, c1: float, c2: float, max_velocity: float, weight: float) -> None:
        self.neighborhood = 0
        self.c1 = c1
        self.c2 = c2
        self.max_velocity = max_velocity
        self.weight = weight
        self.map = map
        self.population: List[Particle] = []
        self.objective = map.get_goal_coords()

    def initial_population(self, population_len: int):
        starting_coords = self.map.get_starting_coords()
        self.neighborhood = population_len
        new_population = []
        for _ in range(population_len):
            new_population.append(
                Particle(choice(starting_coords), goal=self.objective))
        self.population = new_population

    def sort_closest(self, particle: Particle):
        copy = deepcopy(self.population)
        for i in range(1, len(copy)):
            j = i
            while j > 0 and particle.distance_to(copy[j].get_position()) < particle.distance_to(copy[j-1].get_position()):
                part = copy[j-1]
                copy[j-1] = copy[j]
                copy[j] = part
                j -= 1
        return copy

    def get_nearest(self, particle):
        sorted = self.sort_closest(particle)
        return sorted[:self.neighborhood]

    def min_point(self, list: List[Particle]):
        min_dist = None
        min_point = None
        for n in list:
            eval = n.distance_to(self.objective)
            if min_dist == None or eval < min_dist:
                min_point = n
                min_dist = eval
        return min_point

    def new_velocity(self, particle: Particle, best_particle: Particle) -> Vector:
        inertia = particle.velocity * self.weight
        O1 = uniform(0, self.c1)
        cognitive = (particle.best_position - particle.get_position())*O1
        # cognitive = calc_distance(
        #     particle.best_position, particle.real_pos)*O1

        O2 = uniform(0, self.c2)
        social = (best_particle.get_position()-particle.get_position())*O2
        # social = calc_distance(best_particle.real_pos,
        #                        particle.real_pos)*O2

        velocity = inertia + cognitive + social
        if abs(velocity.X) > self.max_velocity:
            velocity.X = velocity.X * self.max_velocity/abs(velocity.X)
        if abs(velocity.Y) > self.max_velocity:
            velocity.Y = velocity.Y * self.max_velocity/abs(velocity.Y)

        # if abs(velocity) > self.max_velocity:
        #     velocity = velocity * self.max_velocity/abs(velocity)

        return velocity

    def movement(self, particle: Particle):
        pos = particle.get_position()
        pos.X += particle.velocity.X
        pos.Y += particle.velocity.Y
        pos.X = round(pos.X)
        pos.Y = round(pos.Y)
        return pos


    def epoch(self):
        for i in self.population:
            neighbors = self.population[:self.neighborhood]
            minimum = self.min_point(neighbors)
            i.velocity = self.new_velocity(i, minimum)
            new_pos = self.movement(i)

            if(not self.map.is_position_valid(new_pos)):
                new_pos = self.map.last_valid_position(
                    i.get_position(), new_pos)

            i.set_position(new_pos)
            if i.distance_to(self.objective) < i.best_eval:
                i.best_position = new_pos
                i.best_eval = i.evaluate_to(self.objective)

    def run(self, population=20, max_iterations=600, tolerance=4):
        self.initial_population(population)
        generation = 0
        best_indv = self.min_point(self.population)
        while best_indv.distance_to(self.objective) > tolerance and generation < max_iterations:
            self.epoch()
            best_indv = self.min_point(self.population)
            generation += 1
        return best_indv
