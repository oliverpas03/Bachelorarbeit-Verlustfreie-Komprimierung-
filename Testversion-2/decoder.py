import json
import numpy as np 
from numpy.typing import NDArray

import huffman as huff

filename = 'Huffman_tabelle.json'

def read_table_from_file( ) -> dict[int,str]: 
  
    with open(filename, 'r') as file:
         d = json.load(file)

    return d 

def build_tree( codetable: dict[int,str]):
    """ Erstellen von Huffmanbaum aus Codetabelle

    Args:
        codetable (dict[int,str]): _description_

    Returns:
        _type_: _description_
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

def decode_huffman(tree: huff.Node , bytes :bytearray, padding: np.uint8)->NDArray[np.int16]:
    """Dekodieren von Bitfolge als String in einzelne Werte

    Args:
        tree (Node): Wurzel von Huffman-Baum
        bit_string (str): kodierte Nachricht als String 

    Raises:
        ValueError: Falls falsch dekodiert 

    Returns:
        NDArray[np.int16]: Array mit dekodierten Werten
    """

    
    result = []
    node = tree
    final_byte = len(bytes)

    message_bitnumber = np.uint16((len(bytes)*8) - np.uint16(padding ))
    proccesed_bits = 0
    
    for i in range(len(bytes)):

        for j in range(7,-1,-1):
          if proccesed_bits == message_bitnumber:
              #abbrechen wenn alle bits der nchricht betrachtet wuden 
              break
          
          byte = bytes[i]
          #aktuelles bit was betrachtet werden soll aus byte herausfiltern 
          bit = (byte >> j) & 1
          proccesed_bits += 1




          if bit == 0:
            node = node.left
          elif bit == 1:
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
        

     
def decode_deltas( array: NDArray[np.int16] )-> NDArray[np.int16]:
    """ Wiederherstellung der Messwerte aus den Deltas 

    Args:
        array (NDArray[np.int16]): Array mit den Differenzen

    Returns:
        _type_: Array mit den Messwerten
    """
    for i in range( 3,len(array)):
        array[i] = array[i-3] + array[i]
    return array


def decode( bit_string, huffman_tree  , padding: np.uint8  )-> NDArray[np.int16] :
    """_summary_

    Args:
        bit_string (_type_): Kodierte Nachricht
        huffman_tree (_type_, optional): Huffman Baum. Kann mit Hilfe von Einlesen der Codetabelle ertellt werden falls nicht vorhanden
                        

    Returns:
        NDArray[np.int16]: Array mit Messwerten 
    """
    
    if ( huffman_tree == None):
         codetable = read_table_from_file()
         huffman_tree = build_tree(codetable)
     
    
    #Aus Nachricht die Differenzwerte generieren.
    array_differences = decode_huffman(  huffman_tree, bit_string, padding )

    #Aus Differenzen die Messwerte berechen 
    array_data = decode_deltas( array_differences)

    return array_data