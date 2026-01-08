import json
import numpy as np
from numpy.typing import NDArray

import huffman as huff

filename = 'Huffman_tabelle.json'

def read_table_from_file( ) -> dict[int,str]:
    """
    Liest Codetabelle aus definierter Datei ein.
    :return: Dictionary das die Werte und die Huffman -Codes enthält
    """
  
    with open(filename, 'r') as file:
         d = json.load(file)

    return d 

def build_tree( codetable: dict[int,str]):
    """
     Generiert einen Huffmanbaum aus einer eingegebenen Codetabelle

     :param codetable: Huffmantabelle als Dictionary
     :return: Huffman Codebaum bzw. die Wurzel des Huffman Codebaums
    """
     
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

def decode_huffman(tree: huff.Node,  bit_string:str)->tuple[int,int]:


    
    result = 0
    node = tree
    end = 0
    
    for i in range( len(bit_string)) :

      
       
        
        
        if bit_string[i] == "0":
            node = node.left
        elif bit_string[i] == "1":
            node = node.right
        
        # Fehlerbehandlung
        if node is None:
            raise ValueError("Ungültiger Pfad")
        
        # Blatt erreicht?
        if node.left is None and node.right is None:
            result = node.symbol
            end = i+1
            break
    return result, end

def recombine_bits( four_bit : np.int16, twelve_bit: np.int16)->np.int16:

    four_bit_shifted = (four_bit << 12) & 0xF000

    recombined_value = ( four_bit_shifted | twelve_bit)

    return np.uint16(recombined_value).view(np.int16)

def decode_both_huffmans(bit_string: str, tree_4bit, tree_12bit)-> NDArray[np.int16]:

    result = []
    while bit_string != "":
        four_bits, endposition  = decode_huffman(tree_4bit ,bit_string)

        bit_string = bit_string[endposition:]

        twelve_bits , endposition = decode_huffman(tree_12bit,bit_string)

        bit_string = bit_string[endposition:]

        value = recombine_bits(four_bits,twelve_bits)
        result.append(value)
    return result










        

     
def decode_deltas( array ):
    for i in range( 3,len(array)):
        array[i] = array[i-3] + array[i]
    return array


def decode( bit_string, huffman_tree_4bit = None  , huffmantree_12bit = None  ):
     codetable = {}
     if ( codetable == None):
         codetable = read_table_from_file()
         huffman_tree = build_tree(codetable)
     
    

     array_differences = decode_both_huffmans(bit_string , huffman_tree_4bit,huffmantree_12bit)

     array_data = decode_deltas( array_differences)

     return array_data