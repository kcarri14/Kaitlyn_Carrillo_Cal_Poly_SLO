[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/J6THYOSh)
### Lab 12: Implementing a File Explorer System Using N-ary Trees

#### Objective:
In this lab, students will develop a basic file explorer system by implementing a simplified model using N-ary trees. This system will support operations such as searching, inserting, deleting, and moving files and directories within a virtual file system.

#### Background:
A file system can be represented as an N-ary tree, where each node represents a file or a directory. The root node represents the root directory, and each child node represents a file or a subdirectory. This structure allows for efficient organization and retrieval of files and directories.

#### Requirements:

1. **N-ary Tree Implementation**:
   - Begin by implementing a basic N-ary tree. Each node should contain information about the file/directory, such as its name and type (file or directory), and a list of children nodes.

2. **Searching for a File/Directory**:
   - Implement a method to search for a file or directory given a file path. The method should return the node if found or `None` if the file/directory does not exist.
   - Example: `search("home/documents/lab/lab12.py")`

3. **Inserting a New Item**:
   - Implement a method to insert a new file or directory given a file path. If any part of the path does not exist, create the necessary directories.
   - Example: `insert("home/documents/lab/lab12.py")`

4. **Deleting a File/Directory**:
   - Implement a method to delete a specified file or directory given a file path. Ensure that deleting a directory also removes all its contents.
   - Example: `delete("home/documents/lab/lab12.py")`

5. **Moving a File/Directory**:
   - Implement a method to move a file or directory from one location to another given two file paths: the source and the destination.
   - Example: `move("home/documents/lab/lab12.py", "home/lab12.py")`

#### Guidelines:

- **File Path Parsing**: Develop a utility function to parse file paths into individual components (e.g., from `"home/documents/lab/lab12.py"` to `["home", "documents", "lab", "lab12.py"]`).

- **Error Handling**: Include error handling for cases such as invalid paths, attempting to insert a file that already exists, or trying to delete/move a non-existent file.

#### Submission:
Submit your Python script containing the N-ary tree implementation and methods for searching, inserting, deleting, and moving files/directories. 

### Descriptions:

### TreeNode Class
- The `TreeNode` class represents the fundamental structure of both files and directories within our virtual file system. 
- Each node in the tree carries a `name` to identify the file or directory it represents, a boolean flag `isFile` to distinguish between files and directories (where `True` signifies a file, and `False` a directory), and a list of `children` which are also `TreeNode` objects.  
- This list-based approach allows each node to have an arbitrary number of children, making it a flexible representation of the N-ary tree structure used to model our file system hierarchy.

### FileExplorer Class
- The `FileExplorer` class encapsulates the functionality of our virtual file system, utilizing the `TreeNode` class to build and manage the file hierarchy. 
- It provides methods for common file operations such as searching, inserting, deleting, and moving files or directories within the system. The class is initialized with a root `TreeNode` that represents the root directory of the file system. 
- This class demonstrates how to implement and manipulate a complex hierarchical structure using basic principles of tree data structures.

### _find_child Method
- A helper method within the `FileExplorer` class, `_find_child` is used to locate a child node by name within a given parent node's children list. 
- It iterates through the list of children, comparing each child's name to the target name. 
- If a match is found, the method returns the corresponding child `TreeNode` object; otherwise, it returns `None`. 
- This method is crucial for navigating the file system tree, as it supports the search functionality required by other methods in the class.

### search Method
- The `search` method allows users to find a file or directory within the file system given its path. 
- It breaks down the path into individual components and uses the `_find_child` method to navigate through the tree structure from the root to the target node. 
- If the path leads to a valid node, that node is returned; otherwise, `None` is returned, indicating that the file or directory does not exist in the system.

### insert Method
- This method adds a new file or directory to the file system at the specified path. 
- It traverses the tree to the appropriate location using the path components and `_find_child` method. 
- If any part of the path does not exist, it creates the necessary intermediate directories. 
- The method ensures that files and directories are inserted correctly according to their paths, maintaining the integrity of the file system structure.

### delete Method
- The `delete` method removes a file or directory from the file system. 
- It locates the target node and its parent using the given path, then removes the target node from the parent's children list. 
- This operation effectively deletes the target from the file system, along with any of its contents if it is a directory.

### move Method
- This method facilitates moving a file or directory from one location to another within the file system. 
- It first removes the target node from its current location using the `delete` method, then re-inserts it at the new location with the `insert` method. This simulates the move operation, ensuring that the file or directory retains its contents and properties during the transfer.

