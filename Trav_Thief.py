'''

Program Name	:	Travelling Thief Problem - Heuristic Search
Author			:	V.Rajagopal
Description		:	

	The program assumes input for the graph of cities as a dictionary, with each key representing a city (starting with 1), and each value being a list of tuples, (destination, distance_from_source). The list of items is maintained in a dictionary, itemset, which assumes the items to be key value pairs, with the key denoting the item, starting from 1, and the values being a list, where the 1st entry is the profit, 2nd is the weight and the third is a tuple of cities the item is available in.

	Vmax, Vmin are expected to be positive real numbers
	R is expected to be a real number between [0,1]
	The max weight of the knapsack, W, must be a positive real number.

Execution		:	Modify graph, itemset, Vmax, Vmin, R, W as necessary. From a terminal execute the following:
						
						python3 Trav_Thief.py

'''




graph = {
			1:[(2, 35), (3, 20), (4, 45), (5, 10), (6, 90), (7, 20)], 
			2:[(1, 35), (4, 40), (5, 15), (6, 20), (7, 25)], 
			3:[(1, 20), (4, 40), (6, 75)],
			4:[(1, 45), (2, 40), (3, 40), (6, 50), (7, 35)],
			5:[(1, 10), (2, 15), (6, 10)],
			6:[(1, 90), (2, 20), (3, 75), (4, 40), (5, 10), (7, 45)],
			7:[(1, 20), (2,25), (4, 35), (6, 45)]

		}

itemset = {
	
			1:[ 300, 50, (1, 2, 3, 4, 5, 6, 7)],
			2:[ 600, 25, (3, 5, 7)],
			3:[ 200, 100, (1, 2, 4, 6)],
			4:[ 100, 10, (4, 5, 6, 7)],
			5:[ 250, 75, (1, 2, 3)]
}

visited = [0] * len(graph)
shortest_path=[]
path_length=[]
Vmax=15
Vmin=5
R = 0.1
W = 500



'''
Below function implements greedy solution to the shortest path subproblem.
'''

def path(i):
	global graph, visited, path_length, shortest_path
	shortest_path+=[i,]
	if visited!=[1]*len(graph):
		visited[i-1]=1
		min=float("inf")
		small=()
		for edge in graph[i]:
			if visited[edge[0]-1]==0 and edge[1]<min:
				small=edge
		if small!=():
			path(small[0])
			path_length+=[small[1]+ (path_length[-1] if len(path_length)>0 else 0) , ]
		else:
			if shortest_path[0] in [x[0] for x in graph[i]]:
				shortest_path+=[shortest_path[0],]
				for x in graph[i]:
					if x[0]==shortest_path[0]:
						path_length+=[x[1] + (path_length[-1] if len(path_length)>0 else 0), ]
			return
				
	else:
		return



'''
Run the path() function until one complete circuit is formed.
'''

for i in range(1, len(graph)+1):
	path(i)
	if shortest_path[0]==shortest_path[-1]:
		break

'''
In distances[], we store the distance of the ith city along the path from the end of the circuit.
'''

distances=[path_length[-1]+path_length[0]-x for x in path_length]

finalitemset=[]
time = path_length[-1]*2*(Vmax+Vmin)			# Time is calculated assuming average velocity throughout the tour.


'''
We assign a score to each item (to each instance of the item in the different cities), that is a measure of the item's worth, taking into account factors like weight, and rent rate of knapsack. This is the heuristic measure for the items.

'''
for key, value in itemset.items():
	for i in value[2]:
		score = int(value[0] - (0.25*value[0]*(distances[shortest_path.index(i)]/path_length[-1])) - (R*time*value[1]/W))
		finalitemset += [[key, i, value[1], score, value[0]], ]

finalitemset.sort(key=lambda x: int(x[3]))		#We sort the items by their score, and then keep picking till the knapsack's weight limit is reached.
finalitemset.reverse()

wc=0
i=0
picked_items=[]
totalprof=0

while i<len(finalitemset):
	if wc+finalitemset[i][2] <= W:
		picked_items+=[[finalitemset[i][0], finalitemset[i][1] ], ]
		wc+=finalitemset[i][2]
		totalprof+=finalitemset[i][4]
	i+=1

# Text manipulation to display user result.

picked_items.sort(key=lambda x: int(x[0]))
values = sorted(set(map(lambda x:x[0], picked_items)))

fin=[]
for i in values:
	tlist=[ ]
	for x in picked_items:
		if x[0]==i:
			tlist+=[x[1], ]
	tlist.sort()
	fin+=[[i, tlist ], ]


print(shortest_path)
print("Total Distance : " + str(path_length[-1]))
print("Thief should take the following items:")
for i in fin:
	print("City : " + str(i[0]) + "   Items : " + ', '.join(str(e) for e in i[1]) )

print("Total profit : " + str(totalprof))
print("Weight carried in knapsack : " + str(wc))