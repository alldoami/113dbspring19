import collections
from string import ascii_lowercase
from string import ascii_uppercase
import unittest
from flask import Flask

app = Flask(__name__)

all_nodes = {}

class TestDijkstra(unittest.TestCase):
    def testAddNode(self):
        print("testaddnode")
        #Testing all letters
        for c in ascii_lowercase:
            self.assertEqual(AddNode(c), c)

        #Testing attempt to add an already existant node
        self.assertEqual(AddNode('a'), "Node a already in graph")

    def testAddRoute(self):
        print("testAddRoute")
        i = 0
        #Testing to add routes to all
        while i < len(ascii_lowercase)-1:
            self.assertEqual(AddRoute(ascii_lowercase[i], ascii_lowercase[i+1], 1), ascii_lowercase[i] + '->' + ascii_lowercase[i+1]+ ': ' + str(1))
            i += 1
        i = 0
        #Trying to Add Routes to Nodes that don't exist
        self.assertEqual(AddRoute(ascii_uppercase[i], ascii_uppercase[i+1], 1), "Invalid route")
    
    def testGetFastestRoute(self):
        print("testGetFastestRoute")
        #Test One Node
        self.assertEqual(GetFastestRoute('a', 'a'), 'Not a possible route')

        #Test Two Nodes
        self.assertEqual(GetFastestRoute('a', 'b'), '"route":"a->b", \n"distance":1')

        #Test Multiple Nodes
        self.assertEqual(GetFastestRoute('a', 'd'), '"route":"a->b->c->d", \n"distance":3')

        #Example Given in Specs:
        AddNode('A')
        AddNode('B')
        AddNode('C')
        AddNode('D')
        AddNode('E')
        AddRoute('B', 'D', 10)
        AddRoute('B', 'C', 5)
        AddRoute('A', 'B', 4)
        AddRoute('A', 'C', 2)
        AddRoute('C', 'E', 3)
        AddRoute('E', 'D', 4)
        AddNode('F')
        AddRoute('D', 'F', 11)
        self.assertEqual(GetFastestRoute('A', 'F'), '"route":"A->C->E->D->F", \n"distance":20')

        #Test Invalid Nodes (one that doesn't exist)
        self.assertEqual(GetFastestRoute('a', '8'), 'Not a possible route')

        #Test Invalid Route (backwards)
        self.assertEqual(GetFastestRoute('z', 'a'), 'Not a possible route')

@app.route("/AddNode/<string:name>/")
def AddNode(name):
    if name not in all_nodes:
        all_nodes[name] = {}
        return name
    return "Node " + name + " already in graph"

@app.route("/AddRoute/<string:firstNode>/<string:secondNode>/<int:length>/")
def AddRoute(firstNode, secondNode, length):
    if firstNode in all_nodes and secondNode in all_nodes:
        all_nodes[firstNode][secondNode] = length
        return firstNode + "->" + secondNode + ": " + str(length)
    return "Invalid route"

@app.route("/GetFastestRoute/<string:start>/<string:end>/")
def GetFastestRoute(start, end):
    if start not in all_nodes.keys() or end not in all_nodes.keys():
        return "Not a possible route"
    distance = {}
    distance[start] = 0
    route = {}
    q = collections.deque()

    #Giving all nodes (besides the start) a temporary distance of infinity
    #(meaning they haven't been visited yet)
    for key, value in all_nodes.items():
        if key != start:
            distance[key] = float("inf")
        q.append(key)

    #Go through queue of nodes and assign shortest path to each node
    while q:
        #Need to sort distance dict because we want to find the node with the shortest tentative distance and
        #set it as the current node
        list_distance = sorted(distance.items(), key=lambda kv: kv[1])
        for i in range(len(list_distance)):
            if list_distance[i][0] in q:
                v = list_distance[i][0]
                q.remove(v)
                break

        #Goes through the nodes connected to the current node and finds the shortest path
        for key, value in all_nodes[v].items():
            d = distance[v] + value
            if d < distance[key]:
                if v != start:
                    route[key] = route[v] + '->' + key
                else:
                    route[key] = v + '->' + key
                distance[key] = d

    #Return found shortest route to end point or return not a possible route if nothing was found
    try:
        return '"route":"' + route[end] + '", \n"distance":' + str(distance[end])
    except:
        return "Not a possible route"

def main():
    AddNode('A')
    AddNode('B')
    AddNode('C')
    AddNode('D')
    AddNode('E')
    AddRoute('B', 'D', 10)
    AddRoute('B', 'C', 5)
    AddRoute('A', 'B', 4)
    AddRoute('A', 'C', 2)
    AddRoute('C', 'E', 3)
    AddRoute('E', 'D', 4)
    AddNode('F')
    AddRoute('D', 'F', 11)
    d = GetFastestRoute('A', 'F')
    print(d)

if __name__ == "__main__":
    #Runs main()
    #main()

    #Runs Unit tests
    #unittest.main()

    #Runs Http server at http://127.0.0.1:5000
    app.run()