from random import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

class City(object):
    city_counter = 0
    
    def __init__(self, location):
        self.id = City.city_counter
        City.city_counter += 1
        self.location = location
        self.neighbors = []
        self.neighbors_distance = []
        self.reference = (0,0)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def add_neighbor_dist(self, distance):
        self.neighbors_distance.append(distance)

    def get_neighbors(self):
        return self.neighbors

    def get_neighbors_distance(self):
        return self.neighbors_distance

    def __cmp__(self, other):
        return self.__dict__ == other.__dict__

# Generates the location of a city that is not too close to any of the others.
# In other words, whenever a city is created, it is at least epsilon distance
# from the rest
def generate_city(cities, epsilon):
    x_pos = random()
    y_pos = random()

    new_city = (x_pos, y_pos)

    for city in cities:
        if get_distance_between(city, new_city) < epsilon:
            return generate_city(cities, epsilon)

    return new_city

# Calculates the Euclidean distance between two cities
def get_distance_between(city, other_city):
    # Euclidean distance
    return ((city[0] - other_city[0])**2 + \
                (city[1] - other_city[1])**2)**(1/2)

# Generates all the cities in the unit square with a distance of at least epsilon
# between them
def generate_cities(num_of_cities, epsilon):
    cities = []
    for i in range(num_of_cities):
        cities.append(generate_city(cities, epsilon))
    return cities

def generate_instance(num_of_cities, epsilon):
    city_locations = generate_cities(num_of_cities, epsilon)
    cities = []

    for location in city_locations:
        cities.append(City(location))

    for city in cities:
        for other_city in cities:
            if city != other_city:
                city.add_neighbor(other_city)
                city.add_neighbor_dist(get_distance_between(city.location, other_city.location))

    return cities

def plot_graph(cities):
    x = []
    y = []
    for city in cities:
        x.append(city.location[0])
        y.append(city.location[1])

    plt.plot(x, y, "o")

    for city in cities:
        for neighbor in city.get_neighbors():
            plt.plot([city.location[0], neighbor.location[0]], [city.location[1], neighbor.location[1]], 'k-')
    plt.savefig('AllCitiesEdges.png')
    plt.show()

all_cities = generate_instance(5, 0.2)
plot_graph(all_cities)

##############################################################################
##############################################################################
##############################################################################

#class representation of an edge
class Path(object):
    
    def __init__(self, a, b, cost):
        self.a = a
        self.b = b
        self.cost = cost

#get the edge set based on the class City
def calculate_edge_set(graph):
    edge_set = []
    checked_cities = []
    for city in graph:
        a = city
        for b in city.neighbors:
            if (b in checked_cities or b not in graph):
                continue
            cost = get_distance_between(a.location, b.location)
            an_edge = Path(a, b, cost)
            edge_set.append(an_edge)
            checked_cities.append(a)
    
    return edge_set

#calculate the minimim spanning tree from a graph defined by an array of class City
def calculate_MST(graph):
    
    if (len(graph) == 0 or len(graph)== 1):
        return []
     
    #get all the edges as a Path object array
    edge_set = calculate_edge_set(graph)
    #sort edges by path cost
    #array of tuples 
    edge_costs = []
    for i in range(len(edge_set)):
        edge_costs.append((i, edge_set[i].cost))
    
    sorted_by_edge_cost = sorted(edge_costs, key=lambda tup: tup[1])    

    #Kruskal's Algorithm    
    #traverse increasing order edge, if they create a cycle, don't add it
    array_set = []
    MST_edges = []
    for i in range(len(sorted_by_edge_cost)):
        index = sorted_by_edge_cost[i][0]
        consider_edge = edge_set[index]
        node_a = consider_edge.a
        node_b = consider_edge.b
        node_a_in_a_set = False
        node_b_in_a_set = False
        for j in range(len(array_set)):
            if (node_a in array_set[j]):
                node_a_in_a_set = True
                node_a_set_ind = j
            if (node_b in array_set[j]):
                node_b_in_a_set = True
                node_b_set_ind = j
        if (node_a_in_a_set == True and node_b_in_a_set == False):
            array_set[node_a_set_ind].append(node_b)
            MST_edges.append(consider_edge)
        elif (node_a_in_a_set == False and node_b_in_a_set == True):
            array_set[node_b_set_ind].append(node_a)
            MST_edges.append(consider_edge)
        elif (node_a_in_a_set == False and node_b_in_a_set == False):
            array_set.append([node_a, node_b])
            MST_edges.append(consider_edge)
        elif (node_a_in_a_set == True and node_b_in_a_set == True):
            if (node_a_set_ind == node_b_set_ind):
                #this causes a cycle, so we can't add this to our edge set
                pass
            else: #(node_a_set_ind != node_b_set_ind)
                set1 = array_set[node_a_set_ind]
                set2 = array_set[node_b_set_ind]
                del array_set[node_a_set_ind]
                for j in range(len(array_set)):
                    if (node_b in array_set[j]):
                        del array_set[j]
                        break
                array_set.append(set1+set2)
                MST_edges.append(consider_edge)
    
    return MST_edges

#claculate the cost based on edge set defined by an array of class Path
def calculate_MST_cost(MST):
    #calculate the sum of the edge costs        
    MST_sum_cost = 0
    for edge in MST:
        MST_sum_cost = MST_sum_cost + edge.cost
    return MST_sum_cost

#plot the minimum spanning tree
def plot_MST (graph, MST_edges):
    x = []
    y = []
    for city in graph:
        x.append(city.location[0])
        y.append(city.location[1])
        
    plt.plot(x, y, "o")
    
    for edge in MST_edges:
        plt.plot([edge.a.location[0], edge.b.location[0]], [edge.a.location[1], edge.b.location[1]], 'k-')
    plt.savefig('MST.png')
    plt.show()


minspantree = calculate_MST(all_cities)
plot_MST(all_cities, minspantree)

class FrontierNode(object):
    def __init__(self, processed, toprocess, process, neighbors_dist, g_n, h_n):
        self.processed = processed #array
        self.toprocess = toprocess #array
        self.process = process #single element
        self.neighbors_dist = neighbors_dist #array
        self.g_n = g_n #single element
        self.h_n = h_n
        self.f_n = g_n+h_n
        self.reference = (0,0)


def A_star_using_MST (city_graph):
    start = time.time()
    
    frontier = []
    #can technically start at any city
    PC = [] #processed city
    IPC = city_graph[0] #in process city
    #get the indices of the city_graph that are yet to be processed
    #to process neighbors
    TPN = [city for city in IPC.neighbors if city not in PC and city != IPC]
    #valid neighbours distance
    VND = [IPC.neighbors_distance[i] for i in range(len(IPC.neighbors)) \
                                if IPC.neighbors[i] not in PC and IPC.neighbors[i] != IPC]
    #immediate_neighbors_dist = 
    g = 0
    h = calculate_MST_cost(calculate_MST(city_graph))
    
    root = FrontierNode(PC, TPN, IPC, VND, g, h)
    
    frontier.append(root)
    
    BestFN = FrontierNode([], [], 0, [], float('inf'), 0)
    
    nodes_expanded = 0
    while(True):
        #pick the item with the min f-value in frontier node
        min_f_FN = frontier[0] #frontier node with minimum f-value
        frontier.pop(0) #remove the minimum node which is always at the first value
        #create a new frontier for each of it's neighbours
        for new_city in min_f_FN.toprocess:
            PC = min_f_FN.processed + [min_f_FN.process]
            IPC = new_city
            #to process neighbors
            TPN = [city for city in IPC.neighbors if city not in PC and city != IPC]
            VND = [IPC.neighbors_distance[i] for i in range(len(IPC.neighbors)) \
                                if IPC.neighbors[i] not in PC and IPC.neighbors[i] != IPC]
            g = min_f_FN.g_n + min_f_FN.neighbors_dist[min_f_FN.toprocess.index(new_city)]
            h = calculate_MST_cost(calculate_MST(TPN))
            
            FN = FrontierNode(PC, TPN, IPC, VND, g, h)
            
            if (len(frontier) != 0):
                if (FN.f_n < frontier[0].f_n):
                    frontier.insert(0, FN)
                elif (FN.f_n > frontier[-1].f_n):
                    frontier.insert(len(frontier), FN)
                else:
                    for i in range(len(frontier)):
                        if (frontier[i].f_n > FN.f_n):
                            frontier.insert(i-1, FN)          
            else:
                frontier.append(FN)
                
            nodes_expanded = nodes_expanded + 1
        
        
        #check if we have found a solution for all paths
        to_pop = []        
        for i in range(len(frontier)):
            if (frontier[i].h_n == 0):
                FN_check = frontier[i]
                to_pop.append(FN_check)
                if (FN_check.g_n < BestFN.g_n):
                    BestFN = FN_check
        frontier = [node for node in frontier if node not in to_pop]
        
        #break if there is no better possible solution
        break_cond = True
        for node in frontier:
            if (node.f_n < BestFN.f_n):
                break_cond = False
        if (break_cond == True):# and len(BestFN.processed) > len(city_graph)-2):
            break
        
        
        
    stop = time.time()
    total_time = stop-start
    
    return [nodes_expanded, total_time]



X = []
Y1 = []
Y2 = []
for test in range(2,5):
    for j in range(5):
        cities = generate_instance(test, 0.2)
        a = A_star_using_MST (cities)
        X.append(test)
        Y1.append(a[0])
        Y2.append(a[1]) 

        
plt.plot(X, Y1, "o")
plt.xlabel('Number of cities')
plt.ylabel('Nodes expanded')
plt.savefig('SalesManNodesExpanded.png')
plt.show()

plt.plot(X, Y2, "o")
plt.xlabel('Number of cities')
plt.ylabel('Time')
plt.savefig('SalesManTime.png')
plt.show()