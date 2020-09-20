import numpy as np

class Graph():
    def __init__(self, vertices):  
        self.graph = [[0 for column in range(vertices)] 
                            for row in range(vertices)]  
        self.V = vertices  
  
    ''' Check if this vertex is an adjacent vertex  
        of the previously added vertex and is not  
        included in the path earlier '''
    def isSafe(self, v, pos, path):  
        # Check if current vertex and last vertex  
        # in path are adjacent  
        if self.graph[ path[pos-1] ][v] == 0:  
            return False
  
        # Check if current vertex not already in path  
        if v in path:  
            return False
  
        return True
  
    # A recursive utility function to solve  
    # hamiltonian cycle problem  
    def hamCycleUtil(self, path, pos):
        # base case: if all vertices are  
        # included in the path  
        if pos == self.V:  
            # Last vertex must be adjacent to the  
            # first vertex in path to make a cyle  
            if self.graph[ path[pos-1] ][ path[0] ] == 1:  
                return True
            else:  
                return False
  
        # Try different vertices as a next candidate  
        # in Hamiltonian Cycle. We don't try for 0 as  
        # we included 0 as starting point in hamCycle()  
        for v in range(1,self.V):  
  
            if self.isSafe(v, pos, path) == True:  
  
                path[pos] = v  
  
                if self.hamCycleUtil(path, pos+1) == True:  
                    return True
  
                # Remove current vertex if it doesn't  
                # lead to a solution  
                path[pos] = -1
  
        return False
  
    def hamCycle(self):  
        path = [-1] * self.V  
  
        ''' Let us put vertex 0 as the first vertex  
            in the path. If there is a Hamiltonian Cycle,  
            then the path can be started from any point  
            of the cycle as the graph is undirected '''
        path[0] = 0
  
        if self.hamCycleUtil(path,1) == False:  
            print ("Solution does not exist\n") 
            return False
  
        self.printSolution(path)  
        return True
  
    def printSolution(self, path):  
        print ("Solution Exists: Following", 
                 "is one Hamiltonian Cycle") 
        for vertex in path:  
            print (vertex, end = " ") 
        print (path[0], "\n") 

height = 40
width = 50
g1 = Graph(height*width)
nodes = g1.V
grid = np.arange(height*width).reshape(height,width)
"""
matrix = []
for i in range(g1.V):
    row = []
    for j in range(g1.V):
        ic =  list(zip(*np.where(grid == i)))
        jc =  list(zip(*np.where(grid == j)))
        if i == j:
            row.append(0)
        elif (jc[0][0] + 1, jc[0][1]) == ic[0] and (ic[0][0] % 2 == 0 or ic[0][0] == 0):
            row.append(1)
        elif  (jc[0][0] - 1, jc[0][1]) == ic[0]:
            row.append(1)
        elif  (jc[0][0], jc[0][1] + 1) == ic[0] and ic[0][1] != 1 and ic[0][0] > 0 and ic[0][0] < height - 1:
            row.append(1)
        elif  (jc[0][0], jc[0][1] - 1) == ic[0]:
            row.append(1)
        elif (ic[0][0] + 1, ic[0][1]) == jc[0] and (jc[0][0] % 2 == 0 or jc[0][0] == 0):
            row.append(1)
        elif  (ic[0][0] - 1, ic[0][1]) == jc[0]:
            row.append(1)
        elif  (ic[0][0], ic[0][1] + 1) == jc[0] and jc[0][1] != 1 and jc[0][0] > 0 and jc[0][0] < height - 1:
            row.append(1)
        elif  (ic[0][0], ic[0][1] - 1) == jc[0]:
            row.append(1)
        else:
            row.append(0)
    matrix.append(row)


#for row in matrix:
    #print(row)

g1.graph = matrix

# Print the solution  
g1.hamCycle();  
"""
# 4x5, 40x50, 25x20
hamiltonian_path = []
for i in range(1, height + 1):
    if i == 1:
        for j in range(1, width + 1):
            hamiltonian_path.append((i, j))
    elif i == height:
        for j in range(width, 0, -1):
            hamiltonian_path.append((i, j))
    elif  i % 2 == 0:
        for j in range(width, 1, -1):
            hamiltonian_path.append((i, j))
    elif i % 2 != 0:
        for j in range(2, width + 1):
            hamiltonian_path.append((i, j))
    

for e in range(height - 1, 0, -1):
    hamiltonian_path.append((e, 1))


def get_action(next_cell, current_cell):
    if next_cell == (current_cell[0] - 1, current_cell[1]):
        return 'up'
    elif next_cell == (current_cell[0] + 1, current_cell[1]):
        return 'down'
    elif next_cell == (current_cell[0], current_cell[1] + 1):
        return 'right'
    else:
        return 'left'
    
    print("error: no action")
    return None
