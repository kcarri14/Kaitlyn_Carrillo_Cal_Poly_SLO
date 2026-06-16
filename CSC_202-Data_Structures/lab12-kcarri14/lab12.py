class TreeNode:
    def __init__(self, name, isFile=False):
        # The name attribute represents the name of the file or directory.
        self.name = name
        # The isFile attribute is a boolean indicating whether the node is a file (True) or directory (False).
        self.isFile = isFile
        # The children attribute holds a list of TreeNode objects representing the node's children.
        self.children = []
        # This is where the N-ary tree structure comes into play, allowing each node to have multiple children.
        # This should be initialized as an empty list.


class FileExplorer:
    def __init__(self):
        self.root = TreeNode("/", isFile=False)

    def _find_child(self, parent, name):
        for child in parent.children:
            if child.name == name:
                return child
        return None

    def search(self, path):
        path_parts = path.strip("/").split("/")
        current = self.root
        for part in path_parts:
            if part:
                current = self._find_child(current, part)
                if current is None:
                    return None
        return current


    def insert(self, path, isFile=False):
        path_parts = path.strip("/").split("/")
        current = self.root
        for part in path_parts[:-1]:
            if part:
                child = self._find_child(current, part)
                if child is None:
                    child = TreeNode(part, True if "." in part else False)
                    current.children.append(child)
                current = child
        if path_parts:
            filename = path_parts[-1]
            child = TreeNode(filename,isFile)
            current.children.append(child)

    def delete(self, path):
        path_parts = path.strip("/").split("/")
        parent = self.search("/".join(path_parts[:-1]))
        filename = path_parts[-1]
        if parent:
                current = self._find_child(parent,filename)
                if current:
                    parent.children.remove(current)
 

    def move(self, source_path, destination_path):
        node = self.search(source_path)
        if node:
            self.delete(source_path)
            self.insert(destination_path)

    
       

    

        



"""#Example Usage
explorer = FileExplorer()
explorer.insert("home/documents/lab/lab12.py", isFile=True)
explorer.insert("home/music")

print(explorer.search("home/documents/lab/lab12.py") is not None)  # True
print(explorer.search("home/music") is not None)  # True

explorer.delete("home/documents/lab/lab12.py")
print(explorer.search("home/documents/lab/lab12.py") is not None)  # False

explorer.move("home/music", "home/documents/music")
print(explorer.search("home/music") is not None)  # False
print(explorer.search("home/documents/music") is not None)  # True
"""
