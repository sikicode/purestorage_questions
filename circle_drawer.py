''' Pure storage:
    Given a parameter r2, where the equation x^2+y^2=r2 holds.
    Return a list of points that 
        (1) x and y are both integers
        (2) fits the circle equation
'''

def find_circle_points(r2):
    """
    Find all integer points (x,y) that satisfy x^2 + y^2 = r2
    
    Args:
        r2 (int): The square of the radius
        
    Returns:
        list: List of tuples (x,y) representing points on the circle
    """
    points = []
    # We only need to check from -sqrt(r2) to sqrt(r2)
    bound = int(r2 ** 0.5)
    
    # Check all possible x values in range
    for x in range(-bound, bound + 1):
        # For each x, calculate what y would need to be
        y2 = r2 - x*x
        # If y2 is a perfect square, we found valid y values
        if y2 >= 0:
            y = int(y2 ** 0.5)
            if y*y == y2:  # Verify it's a perfect square
                # Add both positive and negative y values if y != 0
                points.append((x, y))
                if y != 0:
                    points.append((x, -y))
    
    return sorted(points)

# Example usage
if __name__ == "__main__":
    # Test with r2 = 25 (circle with radius 5)
    r2 = 25
    points = find_circle_points(r2)
    print(f"Integer points on circle with r^2 = {r2}:")
    print(points)
    # Expected output for r2=25: [(-5, 0), (-4, -3), (-4, 3), (-3, -4), (-3, 4), 
    #                             (0, -5), (0, 5), (3, -4), (3, 4), (4, -3), (4, 3), (5, 0)]