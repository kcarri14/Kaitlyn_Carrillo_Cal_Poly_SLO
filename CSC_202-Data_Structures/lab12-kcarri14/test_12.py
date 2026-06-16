import unittest
from lab12 import TreeNode, FileExplorer  # Assume your implementation is in file_explorer.py

class TestTreeNode(unittest.TestCase):
    def test_initialization(self):
        node = TreeNode("test", isFile=True)
        self.assertEqual(node.name, "test")
        self.assertTrue(node.isFile)
        self.assertEqual(node.children, [])

class TestFileExplorer(unittest.TestCase):
    def setUp(self):
        self.explorer = FileExplorer()

    def test_insert_and_search(self):
        self.explorer.insert("home/documents/lab/lab12.py", isFile=True)
        self.assertIsNotNone(self.explorer.search("home/documents/lab/lab12.py"))
        self.assertIsNone(self.explorer.search("home/music/song.mp3"))

    def test_delete(self):
        self.explorer.insert("home/documents/lab/lab12.py", isFile=True)
        self.explorer.delete("home/documents/lab/lab12.py")
        self.assertIsNone(self.explorer.search("home/documents/lab/lab12.py"))

    def test_move(self):
        self.explorer.insert("home/documents/lab/lab12.py", isFile=True)
        self.explorer.move("home/documents/lab/lab12.py", "home/lab12.py")
        self.assertIsNone(self.explorer.search("home/documents/lab/lab12.py"))
        self.assertIsNotNone(self.explorer.search("home/lab12.py"))

    def test_insert_directory_and_file(self):
        self.explorer.insert("home/documents/lab", isFile=False)
        self.explorer.insert("home/documents/lab/lab12.py", isFile=True)
        lab_node = self.explorer.search("home/documents/lab")
        self.assertFalse(lab_node.isFile)
        lab12_node = self.explorer.search("home/documents/lab/lab12.py")
        self.assertTrue(lab12_node.isFile)
if __name__ == '__main__':
    unittest.main()




if __name__ == '__main__':
    unittest.main()
