import math
import heapq
import sys

def readFile():
	content = list()
	
	with open("dados.txt", "r", encoding='UTF-8') as file:
		content = file.readlines()

	content = [line.strip() for line in content]
	content = [info.split(";") for info in content]
	content.append(["IESB", "-15.836073, -47.912019", "Faculdade", True])
	
	infos = list()
	for id, info in enumerate(content):
		info.append(float(info[1].split(",")[0]))
		info.append(float(info[1].split(",")[1]))
		del info[1]
		info[2] = True if info[2]=="True" else False
		infos.append(info)

	return infos

def distance(X1_lat, Y1_long, X2_lat, Y2_long):
    lat1, lon1 = X1_lat, Y1_long
    lat2, lon2 = X2_lat, Y2_long
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def ordered(queue):
	ordered = list()
	while queue:
		ordered.append(heapq.heappop(queue))
	return ordered

def getMin(list, togo, distances):
	aux = sys.maxsize
	id = -1
	for i in distances:
		if i[0] < aux and i[1] in togo:
			aux = i[0]
			id = i[1]
	return aux, id

def buildTogo(list, visited):
	togo = []
	for i in list:
		if visited[i]:
			togo.append(i)
	return togo

def getDistances(list, g):
	distances = [[]]*(g.getSize())
	for i in list:
		distances[i] = g.dijkstra(i, list)[2]
	return distances

def getList(g):
	list = []
	list.append(g.getSize()-1)
	list += [int(i) for i in input("Defina para quais IDs deseja ir: ").split()]
	return list

def getAuxs(g):
	visited = [True]*g.getSize()
	ordem = []
	ordem.append(g.getName(g.getSize()-1))
	return visited, ordem

def defineOrder(g, distances, list):
	lines, dist = [], []
	total = 0
	visited, ordem = getAuxs(g)
	i = g.getSize()-1
	while True:
		visited[i] = False
		togo = buildTogo(list, visited)
		if not len(togo):
			break
		last = g.users[i]
		x, i = getMin(list, togo, distances[i])
		lines.append((last, g.users[i]))
		dist.append(x)
		total += x
		ordem.append(g.getName(i))
	return ordem, lines, dist, total