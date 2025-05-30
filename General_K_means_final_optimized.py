data = [
    [0, 0],    
    [1, 1],    
    [2, 2],    
    [10, 10],  
    [11, 11],  
    [50, 50]
]

# Compute Euclidean Distance between two points
def computeDistance(point1, point2):
    return (((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5)

# Build distance dictionary for all point pairs
def buildDistanceDictionary(points):
    distance_dict = {}
    for i in range(len(points)):
        for j in range(i, len(points)):
            point_i = tuple(points[i])
            point_j = tuple(points[j])
            distance_dict[(point_i, point_j)] = computeDistance(point_i, point_j)
            distance_dict[(point_j, point_i)] = distance_dict[(point_i, point_j)]
    return distance_dict

# Construct sets G (points within radius r) and E (points within radius 3r) from a center point
def constructGandESets(center_point, radius, points, distance_dict, remaining_points_set):
    G = []
    E = []
    center_tuple = tuple(center_point)
    
    for point in points:
        point_tuple = tuple(point)
        if point_tuple not in remaining_points_set:
            continue  # skip removed points
        
        if center_tuple == point_tuple:
            distance = 0
        else:
            distance = distance_dict.get((center_tuple, point_tuple), 0)
        if distance <= 3 * radius:
            E.append(point)
            if distance <= radius:
                G.append(point)
    return [G, E]

# Return the heaviest disk (center with largest G set)
def findHeaviestDisk(radius, points, distance_dict, remaining_points_set):
    max_G_size = 0
    heaviest_disk = []
    heaviest_center = []
    
    for point in points:
        point_tuple = tuple(point)
        if point_tuple not in remaining_points_set:
            continue  # skip removed points
        
        G, E = constructGandESets(point, radius, points, distance_dict, remaining_points_set)
        if len(G) > max_G_size:
            max_G_size = len(G)
            heaviest_disk = E
            heaviest_center = point
    return [heaviest_disk, heaviest_center]

# Run the algorithm for a given radius and number of disks (k)
def runAlgorithm(radius, num_disks, points, distance_dict_input):
    remaining_points_set = set(tuple(p) for p in points)
    solution_centers = []
    distance_dict = distance_dict_input
    
    while num_disks > 0:
        disk_points, disk_center = findHeaviestDisk(radius, points, distance_dict, remaining_points_set)
        solution_centers.append(disk_center)
        
        for point in disk_points:
            point_tuple = tuple(point)
            remaining_points_set.discard(point_tuple)  # fast O(1) removal from set
            
        num_disks -= 1

    if len(remaining_points_set) == 0:
        return solution_centers
    else:
        return "radius not feasible"

# Binary Search on index of distance_values_sorted
def findMinimumFeasibleRadius(points, num_disks):
    full_distance_dict = buildDistanceDictionary(points)
    distance_values_sorted = sorted(set(full_distance_dict.values()))
    
    # Binary search on index
    left = 0
    right = len(distance_values_sorted) - 1
    best_radius = None
    best_solution = None
    
    while left <= right:
        mid_idx = (left + right) // 2
        radius_candidate = distance_values_sorted[mid_idx]
        
        result = runAlgorithm(radius_candidate, num_disks, points, full_distance_dict)
        
        if result != "radius not feasible":
            # Feasible — try smaller radius
            best_radius = radius_candidate
            best_solution = result
            right = mid_idx - 1
        else:
            # Not feasible — try larger radius
            left = mid_idx + 1

    if best_radius is not None:
        return (best_radius, best_solution)
    else:
        return "No feasible radius found"

# Run
print(findMinimumFeasibleRadius(data, 3))
