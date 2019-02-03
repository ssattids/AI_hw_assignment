import heapq
from random import randint
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Node(object):
	def __init__(self, parent, current_pos, goal_state):
		self.path_cost = 1
		self.parent = parent
		self.current_pos = current_pos
		self.goal_state = goal_state
		if parent is None:
			self.g = 0
		else:
			self.g = self.path_cost + parent.g
		# Using Manhattan distance divided by three
		self.h = (abs(self.goal_state[0] - self.current_pos[0]) + \
							abs(self.goal_state[1] - self.current_pos[1])) / 3
		self.f = self.h + self.g

		self.num_of_ancestors = 0
		if parent is not None:
			self.num_of_ancestors += (parent.num_of_ancestors + 1)

	def __eq__(self, other):
		return self.f == other.f

	def __lt__(self, other):
		if self.f == other.f:
			return self.h < other.h
		else:
			return self.f < other.f

	def __gt__(self, other):
		if self.f == other.f:
			return self.h > other.h
		else:
			return self.f > other.f


def moving_knight(initial_node, goal_state):
	start_time = time.time()
	expanded_nodes = 0
	priority_queue = []
	
	heapq.heappush(priority_queue, initial_node)

	visited = set()

	while len(priority_queue) > 0:
		expanded_nodes += 1
		current_node = heapq.heappop(priority_queue)
		visited.add(current_node.current_pos)
		if current_node.current_pos == goal_state:
			return (expanded_nodes, current_node, time.time() - start_time)
		else:
			neighbors = get_neighbors(current_node, goal_state)
			for neighbor in neighbors:
				if neighbor.current_pos not in visited:
					heapq.heappush(priority_queue, neighbor)
	return None



def get_neighbors(current_node, goal_state):
	neighbors = []
	current_x = current_node.current_pos[0]
	current_y = current_node.current_pos[1]
	# 2 right, 1 up
	neighbors.append(Node(current_node, (current_x + 2, current_y + 1), goal_state))
	# 2 left, 1 up
	neighbors.append(Node(current_node, (current_x - 2, current_y + 1), goal_state))
	# 2 right, 1 down
	neighbors.append(Node(current_node, (current_x + 2, current_y - 1), goal_state))
	# 2 left, 1 down
	neighbors.append(Node(current_node, (current_x - 2, current_y - 1), goal_state))

	# 1 right, 2 up
	neighbors.append(Node(current_node, (current_x + 1, current_y + 2), goal_state))
	# 1 left, 2 up
	neighbors.append(Node(current_node, (current_x - 1, current_y + 2), goal_state))
	# 1 right, 2 down
	neighbors.append(Node(current_node, (current_x + 1, current_y - 2), goal_state))
	# 1 left, 2 down
	neighbors.append(Node(current_node, (current_x - 1, current_y - 2), goal_state))
	return neighbors

def generate_random_goal():
	x_value = randint(-20, 20)
	y_value = randint(-20, 20)
	return (x_value, y_value)

def generate_values_for_plot(ite):
	expanded_nodes_lst = []
	time_to_solution_lst = []
	path_to_solution_lst = []
	for i in range(ite):
		goal_state = generate_random_goal()
		initial_node = Node(None, (0, 0), goal_state)
		expanded_nodes, current_node, time_to_solution = moving_knight(initial_node, goal_state)

		# if round(time_to_solution * 1000, 2) > 5:
		# 	print(current_node.current_pos)

		path_to_solution_lst.append(current_node.num_of_ancestors)
		time_to_solution_lst.append(round(time_to_solution * 1000, 2))
		expanded_nodes_lst.append(expanded_nodes)
	return (path_to_solution_lst, time_to_solution_lst, expanded_nodes_lst)

values = generate_values_for_plot(100)

# expanded nodes vs path to solution
plt.scatter(values[0], values[2])
plt.title('Expanded Nodes vs Length to Solution')
plt.xlabel('Length to Solution')
plt.ylabel('Expanded Nodes')
plt.savefig('expanded.png')
plt.show()

# time to solution vs path to solution
plt.scatter(values[0], values[1])
plt.title('Time to Solution vs Length to Solution')
plt.xlabel('Length to Solution')
plt.ylabel('Time to Solution')
plt.savefig('time.png')
plt.show()

# print("arg1 =")
# arg1 = input()
# print("arg2 =")
# arg2 = input()
# goal_state = (int(arg1), int(arg2))
# initial_node = Node(None, (0, 0), goal_state)
# expanded_nodes, current_node, time_to_solution = moving_knight(initial_node, goal_state)

# print(expanded_nodes)
# print("Moves: " + str(current_node.num_of_ancestors))
# print(time_to_solution * 1000)
# n = current_node
# while n is not None:
# 	print(n.current_pos)
# 	n = n.parent