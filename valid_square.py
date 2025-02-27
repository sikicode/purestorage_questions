"""
To run: python3 /Users/sc/Desktop/purestorage_panel/valid_square.py
Question: Design a function that takes 4 points (x,y coordinates) and return ture if the points form a square.
Example squares
// y                                  y                                  y
// ^                                  ^                                  ^
// |          C                       |          B                       |          D
// |  A                               |  A                               |  B
// |                        OR        |                        OR        |                       ETC
// |                                  |                                  |
// |             D                    |             C                    |             A
// |    B                             |    D                             |    C
// +----------------->x               +----------------->x               +----------------->x

Next Question: Design a function that takes in >= 4 points and returns the number of squares that can be formed 
(i.e. how many groups of 4 points(x,y coordinates) within the input points form a square)
Expectation: The complexity of the extended question should be O(N^3)
"""

def distance(p1, p2):
    """Calculate the squared distance between two points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def is_valid_square(points):
    """Determine if four points form a valid square.
    
    Args:
        points: List of 4 points, where each point is a tuple (x, y)
        
    Returns:
        bool: True if points form a valid square, False otherwise
    """
    if len(points) != 4:
        return False
    
    # Calculate distances between all pairs of points
    distances = []
    for i in range(4):
        for j in range(i + 1, 4):
            distances.append(distance(points[i], points[j]))
    
    # Sort distances to group sides and diagonals
    distances.sort()
    
    # For a valid square:
    # - First 4 distances should be equal (sides)
    # - Last 2 distances should be equal (diagonals)
    # - Diagonals should be larger than sides
    return (
        len(distances) == 6 and
        distances[0] > 0 and
        distances[0] == distances[1] == distances[2] == distances[3] and
        distances[4] == distances[5] and
        distances[4] > distances[0]
    )

def count_valid_squares(points):
    """Count the number of valid squares that can be formed from a set of points.
    
    Args:
        points: List of points, where each point is a tuple (x, y)
        
    Returns:
        int: Number of valid squares that can be formed
    """
    if len(points) < 4:
        return 0
    
    n = len(points)
    count = 0
    
    # For each potential diagonal (formed by two points)
    for i in range(n):
        for j in range(i + 1, n):
            diagonal = distance(points[i], points[j])
            center_x = (points[i][0] + points[j][0]) / 2
            center_y = (points[i][1] + points[j][1]) / 2
            
            # Find potential pairs of points that could form the other two vertices
            for k in range(n):
                if k == i or k == j:
                    continue
                    
                # Check if point k has the correct distance from both diagonal endpoints
                dist_k_i = distance(points[k], points[i])
                dist_k_j = distance(points[k], points[j])
                
                if dist_k_i != dist_k_j:
                    continue
                
                # For each potential fourth point
                for l in range(k + 1, n):
                    if l == i or l == j:
                        continue
                        
                    # Check if these four points form a valid square
                    if is_valid_square([points[i], points[j], points[k], points[l]]):
                        count += 1
    
    return count

# Example usage
if __name__ == "__main__":
    # Basic test cases for is_valid_square
    print("\n=== Basic Square Tests ===\n")
    # Test case 1: Simple square
    square1 = [(0, 0), (1, 0), (1, 1), (0, 1)]
    print("Test case 1 - Simple square:", is_valid_square(square1))  # Should print True
    
    # Test case 2: Rotated square
    square2 = [(0, 0), (2, 2), (0, 4), (-2, 2)]
    print("Test case 2 - Rotated square:", is_valid_square(square2))  # Should print True
    
    # Test case 3: Square with floating point coordinates
    square3 = [(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]
    print("Test case 3 - Float coordinates:", is_valid_square(square3))  # Should print True
    
    print("\n=== Invalid Shape Tests ===\n")
    # Test case 4: Rectangle (not a square)
    rectangle = [(0, 0), (2, 0), (2, 1), (0, 1)]
    print("Test case 4 - Rectangle:", is_valid_square(rectangle))  # Should print False
    
    # Test case 5: Collinear points
    collinear = [(0, 0), (1, 1), (2, 2), (3, 3)]
    print("Test case 5 - Collinear points:", is_valid_square(collinear))  # Should print False
    
    # Test case 6: Zero-area square
    zero_area = [(1, 1), (1, 1), (1, 1), (1, 1)]
    print("Test case 6 - Zero area:", is_valid_square(zero_area))  # Should print False
    
    print("\n=== Count Valid Squares Tests ===\n")
    # Test case 7: Single square with extra points
    points1 = [(0, 0), (1, 0), (1, 1), (0, 1), (2, 0), (2, 1)]
    print("Test case 7 - Single square with extra points:")
    print("Points:", points1)
    print("Number of valid squares:", count_valid_squares(points1))  # Should print 1
    
    # Test case 8: Square with point inside
    points2 = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
    print("\nTest case 8 - Square with internal point:")
    print("Points:", points2)
    print("Number of valid squares:", count_valid_squares(points2))  # Should print 1
    
    # Test case 9: Multiple squares in a grid
    points3 = [(0, 0), (1, 0), (1, 1), (0, 1), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)]
    print("\nTest case 9 - Multiple squares in grid:")
    print("Points:", points3)
    print("Number of valid squares:", count_valid_squares(points3))  # Should print 4
    
    # Test case 10: Empty and minimal cases
    print("\nTest case 10 - Edge cases:")
    print("Empty list:", count_valid_squares([]))  # Should print 0
    print("Three points:", count_valid_squares([(0, 0), (1, 1), (2, 2)]))  # Should print 0