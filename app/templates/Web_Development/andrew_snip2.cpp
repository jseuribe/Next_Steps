#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <list>
using namespace std;
int **get_neighbors(int n)
{
    int **matrix;
    for(int u = 0; u < n; u++)
    {
        for (int v = 0; v < n; v++)   //generating a N x N matrix  based on the # of vertex input
        {
            matrix[u] = new int[n];
        }
    }

    for(int u = 0; u < n; u++)
    {
        for (int v = 0; v < n; v++)   //generating a N x N matrix  based on the # of vertex input
        {
            matrix[u][v] = -1;
        }
    }
    
    for(int i = 0; i < n; i++)
    {
    int neighbors = rand() % (n-1);
    int nodes = 0;
    int weight;
    vector<int> nodes_seen;
    int current_node = 0;
    while(nodes != neighbors)
    {
        current_node = rand() % n;
        bool not_seen = true;
		for(int unsigned j = 0; j < nodes_seen.size(); j++)
		{
			if(nodes_seen[j] == current_node)
            {
				not_seen = false;
				break;
			}
		}
		if(not_seen)
        {
            weight = rand()%10 + 1;
            matrix[i][current_node] = weight;
            matrix[current_node][i] = weight;
            nodes_seen.push_back(current_node);
            nodes++;
        }
        cout << i << "," << current_node <<  matrix[i][current_node] << endl;
    }
    }
    return matrix;
}