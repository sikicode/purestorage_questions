"""O(1) Set Implementation

You are given an array of size N to implement a set data structure. The set should support the following operations:

Insert(x): Insert an element x into the set, where 0 ≤ x < N.
Remove(x): Remove an element x from the set.
Lookup(x): Check if an element x is present in the set.
Clear(): Clear all elements from the set.
Iterate(): Iterate over all elements currently in the set.
All operations should have a time complexity of O(1).

Constraints:
Elements to be stored are integers in the range [0, N-1].
The set should be implemented using arrays of size N.
The operations must be efficient, with all of them running in constant time.
"""

class O1Set:
    def __init__(self, N):
        # Initialize arrays of size N
        self.N = N
        self.dense = [0] * N  # Stores the actual elements
        self.sparse = [0] * N  # Maps elements to their positions in dense array
        self.n = 0  # Number of elements in the set

    def insert(self, x):
        """Insert element x into the set"""
        if not 0 <= x < self.N:
            raise ValueError(f"Element {x} out of range [0, {self.N-1}]")
        
        if not self.lookup(x):
            self.dense[self.n] = x
            self.sparse[x] = self.n
            self.n += 1

    def remove(self, x):
        """Remove element x from the set"""
        if not 0 <= x < self.N:
            raise ValueError(f"Element {x} out of range [0, {self.N-1}]")
        
        if self.lookup(x):
            # Get the position of x in dense array
            pos = self.sparse[x]
            
            # Move the last element to the position of x
            last_elem = self.dense[self.n - 1]
            self.dense[pos] = last_elem
            self.sparse[last_elem] = pos
            
            self.n -= 1

    def lookup(self, x):
        """Check if element x is present in the set"""
        if not 0 <= x < self.N:
            raise ValueError(f"Element {x} out of range [0, {self.N-1}]")
        
        return self.sparse[x] < self.n and self.dense[self.sparse[x]] == x

    def clear(self):
        """Clear all elements from the set"""
        self.n = 0

    def iterate(self):
        """Iterate over all elements in the set"""
        for i in range(self.n):
            yield self.dense[i]

# Example usage
if __name__ == "__main__":
    # Create a set that can store numbers from 0 to 9
    s = O1Set(10)
    
    # Insert some elements
    s.insert(5)
    s.insert(3)
    s.insert(7)
    
    # Print all elements
    print("Elements in set:", list(s.iterate()))
    
    # Check if elements exist
    print("Is 5 in set?", s.lookup(5))
    print("Is 2 in set?", s.lookup(2))
    
    # Remove an element
    s.remove(3)
    
    # Print elements after removal
    print("Elements after removing 3:", list(s.iterate()))
    
    # Clear the set
    s.clear()
    print("Elements after clearing:", list(s.iterate()))