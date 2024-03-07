#include <iostream>
#include <set>
#include <unordered_map>

using namespace std;

class Graph {
private:
    unordered_map<int, set<int>> vertices; // Mapping of vertices to their adjacent vertices

public:
    // Function to add an edge between two vertices
    void addEdge(int v1, int v2) {
        vertices[v1].insert(v2);
        vertices[v2].insert(v1);
    }

    // Function to create a subgraph depending on user's choice
    Graph createSubGraph(set<int> selectedVertices) {
        Graph subGraph;
        for (int v : selectedVertices) {
            for (int neighbor : vertices[v]) {
                if (selectedVertices.count(neighbor) > 0) {
                    subGraph.addEdge(v, neighbor);
                }
            }
        }
        return subGraph;
    }

    // Function to perform graph union
    Graph graphUnion(Graph& otherGraph) {
        Graph unionGraph = *this;
        for (const auto& pair : otherGraph.vertices) {
            for (int v : pair.second) {
                unionGraph.addEdge(pair.first, v);
            }
        }
        return unionGraph;
    }

    // Function to perform graph intersection
    Graph graphIntersection(Graph& otherGraph) {
        Graph intersectionGraph;
        for (const auto& pair : vertices) {
            for (int v : pair.second) {
                if (otherGraph.vertices.count(pair.first) > 0 && otherGraph.vertices[pair.first].count(v) > 0) {
                    intersectionGraph.addEdge(pair.first, v);
                }
            }
        }
        return intersectionGraph;
    }

    // Function to check for a disconnected vertex
    bool isDisconnectedVertex(int v) {
        return vertices.find(v) == vertices.end();
    }

    // Function to find the degree of a node
    int getNodeDegree(int v) {
        return vertices[v].size();
    }

    // Function to find at least one path from given two vertices (using Depth First Search)
    bool hasPath(int source, int destination, set<int>& visited) {
        if (source == destination) {
            return true;
        }
        visited.insert(source);
        for (int neighbor : vertices[source]) {
            if (visited.count(neighbor) == 0 && hasPath(neighbor, destination, visited)) {
                return true;
            }
        }
        return false;
    }

    // Function to display edges
    void displayEdges() {
        cout << "Edges:" << endl;
        for (const auto& pair : vertices) {
            int v = pair.first;
            for (int neighbor : pair.second) {
                if (v < neighbor) { // To avoid duplicate edges
                    cout << v << " - " << neighbor << endl;
                }
            }
        }
    }
};

int main() {
    // Sample usage
    Graph g1, g2;

    // Adding edges to the first graph
    g1.addEdge(1, 2);
    g1.addEdge(2, 3);
    g1.addEdge(3, 4);
    g1.addEdge(4, 1);

    // Adding edges to the second graph
    g2.addEdge(3, 4);
    g2.addEdge(5, 6);

    // Displaying edges of the first graph
    cout << "Edges of the first graph:" << endl;
    g1.displayEdges();

    // Displaying edges of the second graph
    cout << "Edges of the second graph:" << endl;
    g2.displayEdges();

    // Other operations...
    
    // Creating subgraph
    set<int> subGraphVertices = {1, 2, 3};
    Graph subGraph = g1.createSubGraph(subGraphVertices);
    cout << "Edges of the subgraph:" << endl;
    subGraph.displayEdges();

    // Graph union
    Graph unionGraph = g1.graphUnion(g2);
    cout << "Edges of the union graph:" << endl;
    unionGraph.displayEdges();

    // Graph intersection
    Graph intersectionGraph = g1.graphIntersection(g2);
    cout << "Edges of the intersection graph:" << endl;
    intersectionGraph.displayEdges();

    // Check for disconnected vertex
    int disconnectedVertex = 7;
    bool isDisconnected = g1.isDisconnectedVertex(disconnectedVertex);
    cout << disconnectedVertex << " is disconnected: " << (isDisconnected ? "Yes" : "No") << endl;

    // Find degree of a node
    int node = 3;
    cout << "Degree of node " << node << ": " << g1.getNodeDegree(node) << endl;

    // Find at least one path between two vertices
    set<int> pathVisited;
    bool hasPath = g1.hasPath(1, 3, pathVisited);
    cout << "Path from 1 to 3 exists: " << (hasPath ? "Yes" : "No") << endl;

    return 0;
}
