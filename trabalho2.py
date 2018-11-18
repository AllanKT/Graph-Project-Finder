from graph import Graph
from service import *
from pprint import pprint

data = readFile()
g = Graph()
g.addNode(data)

g.buildMap()

while True:
	raio = int(input("Defina o raio de busca: "))
	g.getUsers(raio)
	
	list = getList(g)
	distances = getDistances(list, g)

	ordem, lines, dist, total = defineOrder(g, distances, list)
	print(ordem)

	name = str(ordem) + "Total: " + str(total)
	g.buildMapRoutes(lines, dist, name)


"""
Exemplo de saida
IESB, Pergentino, Pedrinaldino, Heráclio

"""