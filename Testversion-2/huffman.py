import heapq
import numpy as np
import json 
from numpy.typing import NDArray

filename  = 'Huffman_tabelle.json'



class Node:
    def __init__(self, symbol=None, frequency=None, nodes= 1):
        self.symbol = symbol
        self.frequency  = int(frequency)
        self.left = None
        self.right = None
        self.nodes  = int(nodes)
        
    def __lt__(self, other):
         if self.frequency != other.frequency:

            return self.frequency < other.frequency
             
         else:
             return self.nodes < other.nodes

        
    
def calculate_frequencys( data : NDArray[np.int16]) -> NDArray[np.uint16]:
    """ Berechnung der Häufigkeiten mithilfe von numpy.histogram().

    Args:
        data (NDArray[np.int16]): Array mit  Werten deren Häufigkeit betimmt werden soll

    Returns:
        NDArray[np.uint16]: Array das das Vorkommen von allen mögichen 16bit Integer Werte enthält. Rückgabewert muss wahrscheinlich noch angepasst werden 
    """
   
    shifted = (data.flatten()).astype(np.int32) +32768

    hist = np.bincount(shifted, minlength=65536)


   

    return hist



def generate_huffmantree( frequencys : NDArray[np.int16]) -> Node:
    """Erstellen des Huffmanbaumes mithilfe des Arrays an Häufigkeiten 

    Args:
        frequencys (NDArray[np.int16]): Array dessen Werte das Vorkommen des entsprechend verschobenen 16bit Integers in den Daten angibt

    Returns:
        Node: Wurzel des Huffman Baumes 
    """
    heap = []
    test = len(frequencys)
    for i in range(0,len(frequencys)):
        value = i - 32768

        node = Node( symbol= value, frequency = frequencys[i])
        heap.append( node)
    heapq.heapify(heap)
    while( len(heap ) > 1):
        smallest_frequency = heapq.heappop(heap)
        second_smallest_frequency = heapq.heappop(heap)

        new_node = Node( frequency= smallest_frequency.frequency + second_smallest_frequency.frequency , nodes = 1+ smallest_frequency.nodes +second_smallest_frequency.nodes)

        new_node.left = smallest_frequency
        new_node.right = second_smallest_frequency

        heapq.heappush(heap, new_node)
    return heap[0]


def generate_codes(node: Node) -> dict[int, str]:
    """ Generierung der Codetabelle aus dem Baum. Aktuell noch als Dictionary muss noch auf Array verändert werden.

    Args:
        node (Node): Wurzel des Huffman Baumes

    Returns:
        dict[int, str]: Codetabelle als dictionary
    """
    
    codetable = {}
    
    if node is None:
        return codetable
    
    # Stack: (node, code)
    stack = [(node, '')]
    
    while stack:
        current_node, code = stack.pop()
        
        if current_node is not None:
            # Blatt gefunden (Symbol vorhanden)
            if current_node.symbol is not None:
                codetable[current_node.symbol] = code
            
            # Rechts zuerst auf Stack (wird später verarbeitet)
            if current_node.right is not None:
                stack.append((current_node.right, code + '1'))
            
            # Links danach (wird zuerst verarbeitet - DFS)
            if current_node.left is not None:
                stack.append((current_node.left, code + '0'))
    
   # write_table_to_file(codetable)
    test1 = codetable[-32768]
    test2 = codetable[32767]
    return codetable

   

   

def write_table_to_file(codetable : dict[int,str]) -> None:
    """ Speichern von Codetabelle in Datei. Muss noch angepasst werden sodass Array von Codewörtern und deren Länge gespeichert wird  

    Args:
        codetable (dict[int,str]): _description_
    """

  
    with open(filename, 'w') as f:
         json.dump(codetable, f)




    


    