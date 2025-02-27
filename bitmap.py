''' buddy system bitmap
    Given a complete binary tree with nodes of values of either 1 or 0, the following rules always hold:
    (1) a node's value is 1 if and only if all its subtree nodes' values are 1
    (2) a leaf node can have value either 1 or 0
    Implement the following 2 APIs:
    set_bit(offset, length), set the bits at range from offset to offset+length-1
    clear_bit(offset, length), clear the bits at range from offset to offset+length-1
    
    i.e. The tree is like:
                 0
              /     \
             0        1
           /  \      /  \
          1    0    1    1
         /\   / \   / 
        1  1 1   0 1
        Since it's complete binary tree, the nodes can be stored in an array:
        [0,0,1,1,0,1,1,1,1,1,0,1] 
        
'''

class BuddyBitmap:
    def __init__(self, size):
        """Initialize bitmap with given size (number of leaf nodes)"""
        # Calculate total nodes needed for complete binary tree
        self.leaf_count = size
        self.total_nodes = 2 * size - 1
        self.bitmap = [0] * self.total_nodes
    
    def _get_parent(self, index):
        """Get parent index of current node"""
        return (index - 1) // 2 if index > 0 else None
    
    def _get_left_child(self, index):
        """Get left child index of current node"""
        left = 2 * index + 1
        return left if left < self.total_nodes else None
    
    def _get_right_child(self, index):
        """Get right child index of current node"""
        right = 2 * index + 2
        return right if right < self.total_nodes else None
    
    def _update_parent(self, index):
        """Update parent nodes recursively"""
        parent = self._get_parent(index)
        while parent is not None:
            left = self._get_left_child(parent)
            right = self._get_right_child(parent)
            # Parent is 1 only if both children are 1
            self.bitmap[parent] = 1 if (self.bitmap[left] == 1 and 
                (right is None or self.bitmap[right] == 1)) else 0
            parent = self._get_parent(parent)
    
    def _get_leaf_index(self, offset):
        """Convert offset to leaf node index"""
        return offset + self.leaf_count - 1
    
    def set_bit(self, offset, length):
        """Set bits from offset to offset+length-1"""
        if offset < 0 or offset + length > self.leaf_count:
            raise ValueError("Invalid offset or length")
        
        # Set each leaf node in the range
        for i in range(length):
            leaf_idx = self._get_leaf_index(offset + i)
            self.bitmap[leaf_idx] = 1
            self._update_parent(leaf_idx)
    
    def clear_bit(self, offset, length):
        """Clear bits from offset to offset+length-1"""
        if offset < 0 or offset + length > self.leaf_count:
            raise ValueError("Invalid offset or length")
        
        # Clear each leaf node in the range
        for i in range(length):
            leaf_idx = self._get_leaf_index(offset + i)
            self.bitmap[leaf_idx] = 0
            self._update_parent(leaf_idx)

# Example usage
if __name__ == "__main__":
    # Create bitmap with 7 leaf nodes as shown in the example
    bitmap = BuddyBitmap(7)
    
    # Set bits to create the example tree
    bitmap.set_bit(0, 2)  # Set first two leaf nodes to 1
    bitmap.set_bit(4, 1)  # Set fifth leaf node to 1
    bitmap.set_bit(5, 2)  # Set sixth and seventh leaf nodes to 1
    
    print("Bitmap array:", bitmap.bitmap)