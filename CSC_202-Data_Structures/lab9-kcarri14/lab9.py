class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def sortedListToBST(nums):
   if not nums:
        return None
    
   mid = len(nums) // 2
   root = TreeNode(nums[mid])
    
   root.left = sortedListToBST(nums[:mid])
   root.right = sortedListToBST(nums[mid + 1:])
    
   return root


def isValidBST(root, left=float('-inf'), right=float('inf')):
    if not root:
        return True
    
    if not (left < root.value < right):
        return False
    
    return (isValidBST(root.left, left, root.value) and
            isValidBST(root.right, root.value, right))

def areSameTree(p, q):
    if not p and not q:
        return True
    # If one of the roots is None but the other is not, they are not identical
    if not p or not q:
        return False
    # If values are different, they are not identical
    if p.value != q.value:
        return False
    # Recursively check left and right subtrees
    return areSameTree(p.left, q.left) and areSameTree(p.right, q.right)
