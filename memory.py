"""
Memory copy (memcpy) and memory move (memmove) are both functions used for copying memory blocks, 
but they have a key difference in how they handle overlapping memory regions:

1. memcpy:
- Doesn't handle overlapping memory regions safely
- Faster than memmove
- Source and destination must not overlap
- Undefined behavior if regions overlap
2. memmove:
- Safely handles overlapping memory regions
- Slightly slower than memcpy
- Creates a temporary buffer if needed
- Guarantees correct data transfer even with overlap
Use memmove when memory regions might overlap, and memcpy when you're certain they don't overlap 
and want better performance.
"""