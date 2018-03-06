######################################
# Might Be Easier to Use defaultdict #
######################################

# Source:
# Cyclic Check: https://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle
# Graph and Topological Sorting: https://www.geeksforgeeks.org/topological-sorting/

__author__ = 'jbrownlow'

from collections import defaultdict

class Graph:
    """
    Graph: Creates a graph structure using defaultdict

    Functions:
    addEdge:
        - u: Parent
        - v: Child if Exists
        This function creates the graph by using
        default dict to contain the information
        that defines the graph.

    topologicalSort:
        - Returns ordered list based on level
    """

    def __init__(self):
        self.graph = defaultdict(list)
        self.v = [] # All Values Used

    def _get_vertices(self):
        return list(set(self.v))

    def _generate_sorting_dictionary(self):
        v = self._get_vertices()
        return dict(zip(v, [False for _ in v]))

    def _is_cyclical(self):

        visited = set()
        path = [object()]
        path_set = set(path)
        stack = [iter(self.graph)]

        while stack:
            for v in stack[-1]:
                if v in path_set:
                    return True
                elif v not in visited:
                    visited.add(v)
                    path.append(v)
                    path_set.add(v)
                    stack.append(iter(self.graph.get(v, ())))
                    break
            else:
                path_set.remove(path.pop())
                stack.pop()
        return False

    def _topologicalSortUtil(self, v, visited, stack):

        visited[v] = True

        for i in self.graph[v]:
            if visited[i] == False:
                self._topologicalSortUtil(i, visited, stack)

        stack.insert(0, v)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.v.extend([u, v])

    def topologicalSort(self):

        stack = []
        visited = self._generate_sorting_dictionary()

        if self._is_cyclical():
            raise AttributeError('graph cannot be cyclic.')

        for i in self._get_vertices():
            if visited[i] == False:
                self._topologicalSortUtil(i, visited, stack)

        if None in stack:
            stack.remove(None)

        stack.reverse()

        return stack

g = Graph()
g.addEdge("A", "B")
g.addEdge("B", "C")
g.addEdge("A", "C")
g.addEdge("A", "D")
#g.addEdge("C", "A") # Add if cyclic
g.addEdge("E", "F")
g.addEdge("G", "H")
#g.addEdge("G", None) # If No Connection

print(g.graph)
print "Following is a Topological Sort of the given graph"
stack = g.topologicalSort()
print(stack)
