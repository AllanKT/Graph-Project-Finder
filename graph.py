from service import *
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from heapq import heappush, heappop
import sys
import pandas as pd

class Node(object):
	def __init__(self, id, name, job, availability, lat, long):
		self.id = id #int
		self.name = name #string
		self.job = job #string
		self.availability = availability #bool
		self.lat = lat #float
		self.long = long #float


class Graph(object):
	def __init__(self):
		self.graph = dict()
		self.users = list()
		self.distances = list()
		self.all_dist = dict()
		self.x = list()
		self.y = list()
		self.labels = list()

	def addNode(self, content):
		self.build(content)
		for id, node in enumerate(content):
			n = Node(id, node[0], node[1], node[2], node[3], node[4])
			self.users.append(n)	
			self.x.append(node[3])
			self.y.append(node[4])
			self.labels.append(node[0] + "::" + str(node[2]))
			for i in range(len(content)):
				if n.id != i:
					self.graph[i].append((n, distance(n.lat, n.long, content[i][3], content[i][4])))
					self.distances.append((distance(n.lat, n.long, content[i][3], content[i][4]), (n.id, i)))
		self.distances.sort()

	def buildMap(self):
		fig, ax = plt.subplots(figsize=(10, 10), sharey=True)
		for x, y, label in zip(self.x, self.y, self.labels):
			ax.scatter(x, y, alpha=0.7, color=np.random.rand(3), label=label)
		ax.grid()
		ax.legend()
		fig.suptitle('Mapa')
		plt.ioff()
		plt.show()

	def buildMapRoutes(self, lines, dist, name):
		fig, ax = plt.subplots(figsize=(10, 10), sharey=True)
		for x, y, label in zip(self.x, self.y, self.labels):
			ax.scatter(x, y, alpha=0.7, color=np.random.rand(3), label=label)
		for (a, b), c in zip(lines, dist):
			ax.plot((b.lat, a.lat), (b.long, a.long), label=c)
		ax.grid()
		ax.legend()
		fig.suptitle(name)
		plt.ioff()
		plt.show()

	def build(self, content):
		for i in range(len(content)):
			self.graph[i] = list()

	def raioOrigin(self, id):
		return self.graph[self.getSize()-1][id][1]

	def getGraph(self):
		for id, nodes in self.graph.items():
			for node, dist in nodes:
				print(self.users[id].name, node.name, dist)

	def getUsers(self, raio):
		id, name, weight = [], [], []
		for user in self.users:
			if user.id != self.getSize()-1 and self.raioOrigin(user.id) <= raio and user.availability:
				id.append(user.id)
				name.append(user.name)
				weight.append(self.raioOrigin(user.id))
		data = {"ID": id, "Names": name, "Distance": weight}
		df = pd.DataFrame(data=data)
		print(df)

	def getName(self, id = int):
		return self.users[id].name

	def getSize(self):
		return len(self.graph)

	def dijkstra(self, root, togo):
		dist_ans, answer, visited, queue, father = list(), [sys.maxsize for _ in range(self.getSize())], set(), list(), [-1 for _ in range(self.getSize())]
		answer[root], father[root] = 0, root
		visited.add(root)
		queue.append((root, 0))
		while queue:
			queue = ordered(queue)
			vertex, dist = queue[0]
			del queue[0]
			for neighbour, weight in self.graph[vertex]:
				weight_total = weight + dist
				if neighbour.id not in visited or weight_total < answer[neighbour.id]:
					answer[neighbour.id] = weight_total
					father[neighbour.id] = vertex
					visited.add(neighbour.id)
					heapq.heappush(queue, (neighbour.id, answer[neighbour.id]))
					if neighbour.id in togo:
						dist_ans.append((weight_total, neighbour.id))
		return answer, father, dist_ans
