"""File Reverser

This module provides two methods for reversing files:
1. Line-by-line reversal
2. Complete content reversal

Both methods are designed to work with large files under memory constraints.

Follow up:
1. If the file is very large 2. Available memory is very low, how would you approach this challenge?
"""

import os

def reverse_file_by_lines(input_path, output_path, chunk_size=8192):
    """Reverse a file line by line using a memory-efficient approach.
    
    Args:
        input_path (str): Path to the input file
        output_path (str): Path to save the reversed output
        chunk_size (int): Size of chunks to read at a time
    """
    file_size = os.path.getsize(input_path)
    
    # Store newline positions
    newline_positions = []
    with open(input_path, 'rb') as f:
        # Start from the end of file
        pos = file_size
        while pos > 0:
            # Move chunk_size bytes backward
            chunk_end = pos
            chunk_start = max(0, pos - chunk_size)
            size = chunk_end - chunk_start
            
            # Seek to the chunk start and read the chunk
            f.seek(chunk_start)
            chunk = f.read(size)
            
            # Find all newlines in this chunk
            for i in range(size - 1, -1, -1):
                if chunk[i:i+1] == b'\n':
                    newline_positions.append(chunk_start + i)
            
            # If we're at the start of file, add position 0
            if chunk_start == 0:
                newline_positions.append(0)
                
            pos = chunk_start
    
    # Write reversed lines to output file
    with open(input_path, 'rb') as fin, open(output_path, 'wb') as fout:
        # Process each line segment
        for i in range(len(newline_positions)):
            # Calculate line bounds
            line_end = file_size if i == 0 else newline_positions[i-1]
            line_start = newline_positions[i]
            
            # Read and write the line
            fin.seek(line_start)
            line = fin.read(line_end - line_start)
            fout.write(line)

def reverse_file_content(input_path, output_path, chunk_size=8192):
    """Reverse entire file content using a memory-efficient approach.
    
    Args:
        input_path (str): Path to the input file
        output_path (str): Path to save the reversed output
        chunk_size (int): Size of chunks to read at a time
    """
    file_size = os.path.getsize(input_path)
    
    # Create output file of same size
    with open(output_path, 'wb') as f:
        f.seek(file_size - 1)
        f.write(b'\0')
    
    with open(input_path, 'rb') as fin, open(output_path, 'r+b') as fout:
        left = 0
        right = file_size
        
        while left < right:
            # Calculate chunk sizes for both ends
            left_size = min(chunk_size, right - left)
            right_size = min(chunk_size, right - left)
            right_start = right - right_size
            
            # Read chunks from both ends
            fin.seek(left)
            left_chunk = fin.read(left_size)
            fin.seek(right_start)
            right_chunk = fin.read(right_size)
            
            # Write reversed chunks to opposite ends
            fout.seek(right_start)
            fout.write(bytes(reversed(left_chunk)))
            fout.seek(left)
            fout.write(bytes(reversed(right_chunk)))
            
            # Move pointers
            left += left_size
            right -= right_size

# Example usage
if __name__ == "__main__":
    # Create a sample file
    with open("sample.txt", "w") as f:
        f.write("First line\nSecond line\nThird line\n")
    
    # Test line reversal
    reverse_file_by_lines("sample.txt", "reversed_lines.txt")
    print("File reversed by lines saved to 'reversed_lines.txt'")
    
    # Test content reversal
    reverse_file_content("sample.txt", "reversed_content.txt")
    print("File content reversed saved to 'reversed_content.txt'")