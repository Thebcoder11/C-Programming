import os
import re
import urllib.parse

# Folders to ignore
IGNORE = ['.git', '.vscode', '__pycache__', '.github']

def count_c_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.c'):
                count += 1
    return count

def generate_table():
    base_path = '.'
    table = "| 📁 Topic | 📝 Description | 📊 File Count |\n| :--- | :--- | :--- |\n"
    
    # Optional descriptions
    descriptions = {
        'Basic': 'Understand the structure of a C program, `#include`, `printf()`, `scanf()`, variables, and primitive data types.',
        'Conditional Statement': 'Learn to make decisions using `if`, `else if`, `else`, nested conditions, and the `switch-case` statement.',
        'Loops': 'Execute code repeatedly using `for`, `while`, and `do-while` loops.',
        'Pattern Printing': 'Dive into nested loops through classic star (`*`) patterns, number pyramids, and diamond shapes.',
        'Array': 'Learn about 1D data structures to store multiple items of the same type in contiguous memory.',
        '2DArray': 'Matrices and tabular data. Essential for advanced matrix mathematics and dynamic programming setups.',
        'Strings': 'In C, strings are character arrays. Explore `string.h` library functions and custom string manipulations.',
        'Function And Pointer': 'The heart of C! Learn modularity with functions, and direct memory access using pointers. Includes call by value vs. call by reference.',
        'Recursion': 'Functions that call themselves! A beautiful concept for solving problems like factorials, Fibonacci series, and Tower of Hanoi.',
        'Structures': 'Create your own custom data types using `struct`, grouping different data types together.',
        'Sorting': 'Classic sorting algorithms implemented from scratch: Bubble Sort, Selection Sort, Insertion Sort, etc.',
        'FileHandling': 'Read from and write to text and binary files using file pointers (`fopen`, `fprintf`, `fread`, etc.).'
    }
    
    dirs = [d for d in os.listdir(base_path) if os.path.isdir(d) and d not in IGNORE]
    dirs.sort()
    
    for d in dirs:
        count = count_c_files(d)
        desc = descriptions.get(d, 'Various C programming exercises and examples.')
        link = urllib.parse.quote(d)
        table += f"| **[{d}](./{link})** | {desc} | {count} files |\n"
        
    return table

def main():
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace table section
    start_marker = "## 🗂️ Topic Explorer\n\nExplore the repository by navigating through the neatly structured topics. Every folder contains source code and specific examples to learn from.\n\n"
    end_marker = "\n---\n\n## 🚀 Getting Started"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx + len(start_marker)] + generate_table() + content[end_idx:]
        
        # Count total files
        total_files = count_c_files('.')
        # Replace the badge
        new_content = re.sub(
            r'<img src="https://img.shields.io/badge/(Topics|Files)-[^-]+-success\.svg" alt="(Topics|Files)">',
            f'<img src="https://img.shields.io/badge/Files-{total_files}-success.svg" alt="Files">',
            new_content
        )
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("README.md updated successfully!")
    else:
        print("Could not find markers to update.")

if __name__ == '__main__':
    main()
