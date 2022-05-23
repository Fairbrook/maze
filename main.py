import functools
from Coord import Coord
from Differential import DifferentialEvolution
from Genetic import GeneticAlgothm
from Image import draw_path, get_pixels, show_result
from Map import Map
from Individual import Individual
from PSO import Swarm


pixels = get_pixels("./maps/map2.png")
map = Map(pixels)
# de = DifferentialEvolution(map)
# solution = de.run(max_steps=1000, population=300)
pso = Swarm(map, 2.558, 1.3358, 5, 0.3925)
solution = pso.run()
# ga = GeneticAlgothm(map,0.45)
# solution = ga.run()
# x = Individual(Coord(0,0))
# x.set_position(Coord(0,50))
# print(len(pixels))
# show_result(functools.reduce(lambda res, indv: res+indv.get_history(),pso.population,[]), pixels)
# show_result(pso.population[0].get_history(), pixels)
show_result(solution.get_history(), pixels)
