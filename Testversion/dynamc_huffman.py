import csv 

class Node:
    def __init__(self, symbol=None, frequency=None, parent=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.parent = parent

    def __lt__(self, other):
        return self.frequency < other.frequency

    def change_needed(self):
        return self.parent and self.parent.left.frequency > self.parent.right.frequency


def generate_codes(node, code, codetable):
    if node is not None:
        if node.symbol is not None:
            codetable[node.symbol] = code
        generate_codes(node.left, code + [0], codetable)
        generate_codes(node.right, code + [1], codetable)
    return codetable


class Huffman_Code:
    def __init__(self):
        self.root = Node(symbol="NYT", frequency=0)
        self.codes = {"NYT": []}

    def update_tree(self, beginning_node):
        node = beginning_node.parent
        new_codetable_needed = 0
        while node is not None:
            if node.left.frequency + node.right.frequency != node.frequency:
                node.frequency = node.left.frequency + node.right.frequency
                if node.left.frequency > node.right.frequency:
                    node.left, node.right = node.right, node.left
                    new_codetable_needed = 1
            node = node.parent
        if new_codetable_needed:
            self.create_codetable()

    def create_codetable(self):
        new_codetable = {}
        self.codes = generate_codes(self.root, [], new_codetable)
    
    def get_tree_info(self,node, prefix="root"):
      """Helper function to visualize tree structure"""
      if node is None:
        return {}
    
      info = {}
      if node.symbol:
        info[prefix] = f"{node.symbol}:{node.frequency}"
      else:
         info[prefix] = f"internal:{node.frequency}"
    
      if node.left:
        info.update(self.get_tree_info(node.left, prefix + ".L"))
      if node.right:
        info.update(self.get_tree_info(node.right, prefix + ".R"))
    
      return info


def huffman_encode(code, x):
    if x in code.codes.keys():
        path = code.codes[x]
        node = code.root
        for i in path:
            if i == 0:
                node = node.left
            else:
                node = node.right
        node.frequency += 1
        if node.change_needed():
            code.update_tree(node)
    else:
        path = code.codes["NYT"]
        node = code.root
        for i in path:
            if i == 0:
                node = node.left
            else:
                node = node.right
        
        # Create new internal node
        new_parent = Node(frequency=1, parent=node.parent)
        new_node = Node(symbol=x, frequency=1, parent=new_parent)
        
        # Update tree structure
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_parent
            else:
                node.parent.right = new_parent
        else:
            code.root = new_parent
            
        new_parent.left, new_parent.right = node, new_node
        node.parent = new_parent
        
        code.create_codetable()
        
        if new_parent.change_needed():
            code.update_tree(new_parent)
    
    return code.codes[x]




def huffman_decode(code, bit_string):
    result = []
    node = code.root
    
    for bit in bit_string:
      
       
        
        
        if bit == "0":
            node = node.left
        elif bit == "1":
            node = node.right
        
        # Fehlerbehandlung
        if node is None:
            raise ValueError("Ungültiger Pfad")
        
        # Blatt erreicht?
        if node.left is None and node.right is None:
            result.append(node.symbol)
            
            node = code.root
    
    return result
        






