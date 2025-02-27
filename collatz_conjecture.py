"""
Run: python3 collatz_conjecture.py
The Collatz Conjecture 
If you take a positive integer N and repeatedly set either 
1) N=N/2 (if it's even) or
2) N=3N+1 (if it's odd)
N will eventually be 1.
5 -> 16 -> 8 -> 4 -> 2 -> 1 (5 steps).
Given N, how many steps does it take to reach 1?
"""

def collatz_steps(n, memo=None):
    """
    Calculate the number of steps needed to reach 1 using the Collatz conjecture.
    
    Args:
        n (int): The starting positive integer
        memo (dict): Memoization dictionary to store previously calculated results
        
    Returns:
        int: Number of steps to reach 1
        
    Raises:
        ValueError: If n is not a positive integer
    """
    # Input validation
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")
    
    # Initialize memoization dictionary if None
    if memo is None:
        memo = {}
    
    # Base case: n is 1
    if n == 1:
        return 0
    
    # Check if result is already memoized
    if n in memo:
        return memo[n]
    
    # Calculate next number based on whether n is even or odd
    if n % 2 == 0:
        steps = 1 + collatz_steps(n // 2, memo)
    else:
        steps = 1 + collatz_steps(3 * n + 1, memo)
    
    # Store result in memo before returning
    memo[n] = steps
    return steps

# Example usage
test_numbers = [5, 13, 19, 27]
for num in test_numbers:
    try:
        steps = collatz_steps(num)
        print(f"Number {num} takes {steps} steps to reach 1")
    except ValueError as e:
        print(f"Error: {e}")