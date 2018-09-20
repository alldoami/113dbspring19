from flask import Flask
import collections
import unittest
from string import ascii_lowercase
from string import ascii_uppercase

app = Flask(__name__)

allNodes = dict()
allNodes = {}

class TestDijkstra(unittest.TestCase):
    def testAddNode(self):
        print("testaddnode")
        #Testing all letters
        for c in ascii_lowercase:
            self.assertEqual(AddNode(c),c)

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
        AddRoute('B','D',10) 
        AddRoute('B','C',5) 
        AddRoute('A','B',4) 
        AddRoute('A','C',2) 
        AddRoute('C','E',3) 
        AddRoute('E','D',4) 
        AddNode('F') 
        AddRoute('D','F',11) 
        self.assertEqual(GetFastestRoute('A', 'F'), '"route":"A->C->E->D->F", \n"distance":20')

        #Test Invalid Nodes (one that doesn't exist)
        self.assertEqual(GetFastestRoute('a', '8'), 'Not a possible route')

        #Test Invalid Route (backwards)
        self.assertEqual(GetFastestRoute('z', 'a'), 'Not a possible route')

@app.route("/AddNode/<string:name>/")
def AddNode(name):
    if(name not in allNodes):
        allNodes[name] = {}
        return name
    else:
        return "Node " + name + " already in graph"

@app.route("/AddRoute/<string:firstNode>/<string:secondNode>/<int:length>/")
def AddRoute(firstNode, secondNode, length):
    if(firstNode in allNodes and secondNode in allNodes):
        allNodes[firstNode][secondNode] = length
        return firstNode + "->" + secondNode + ": " + str(length)
    else:
        return "Invalid route"

@app.route("/GetFastestRoute/<string:start>/<string:end>/", methods = ['GET'])
def GetFastestRoute(start, end):
    if(start not in allNodes.keys() or end not in allNodes.keys()):
        return "Not a possible route"
    distance = dict()
    distance = {}
    distance[start] = 0
    route = dict()
    route = {}
    q = collections.deque()

    for key, value in allNodes.items():
        if key != start:
            distance[key] = float("inf")
        q.append(key)
    
    while q:
        list_distance = sorted(distance.items(), key=lambda kv: kv[1])
        for i in range(len(list_distance)):
            if list_distance[i][0] in q:
                v = list_distance[i][0]
                q.remove(v)
                break

        for key, value in allNodes[v].items():
            d = distance[v] + value
            if d < distance[key]:
                if (v != start):
                    route[key] = route[v] + '->' + key
                else: 
                    route[key] = v + '->' + key
                distance[key] = d

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
    
    AddRoute('B','D',10) 
    AddRoute('B','C',5) 
    AddRoute('A','B',4) 
    AddRoute('A','C',2) 
    AddRoute('C','E',3) 
    AddRoute('E','D',4) 
    AddNode('F') 
    AddRoute('D','F',11) 
    #AddRoute('A','C', 3)
    #AddRoute('A', 'B', 1)
    #AddRoute('B','C', 1)
    #AddRoute('C', 'D', 1)
    d = GetFastestRoute('A','F')
    print(d)
        
if __name__ == "__main__":
    #main()
    unittest.main()
    #app.run()

                
