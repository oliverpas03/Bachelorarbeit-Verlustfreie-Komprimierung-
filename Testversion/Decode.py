import json

import delta_Huffman as huff

def read_table_from_file( filename) -> dict[int,str]: 
  
    with open(filename, 'r') as file:
         d = json.load(file)

    return d 

def build_tree( codetable: dict[int,str]):
     
     root = huff.Node
     for char, code in codetable.items():
        current = root
        for bit in code:
            if bit == '0':
                if current.left is None:
                    current.left = huff.Node()
                current = current.left
            else:  
                if current.right is None:
                    current.right = huff.Node()
                current = current.right
        
       
        current.char = char
    
     return root
     
