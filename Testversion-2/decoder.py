import json
import numpy as np 

import huffman as huff

filename = 'Huffman_tabelle.json'

def read_table_from_file( ) -> dict[int,str]: 
  
    with open(filename, 'r') as file:
         d = json.load(file)

    return d 

def build_tree( codetable: dict[int,str]):
     
     root = huff.Node()
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
        
       
        current.symbol = char
    
     return root

def decode_huffman(tree , bit_string):

    
    result = []
    node = tree
    
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
            
            node = tree
    array = np.array(result)
    return array
        

     
def decode_deltas( array ):
    for i in range( 3,len(array)):
        array[i] = array[i-3] + array[i]
    return array


def decode( bit_string, codetable = None   ) :
     if ( codetable == None):
         codetable = read_table_from_file()
     
     huffman_tree = build_tree(codetable)

     array_differences = decode_huffman(  huffman_tree, bit_string)

     array_data = decode_deltas( array_differences)

     return array_data