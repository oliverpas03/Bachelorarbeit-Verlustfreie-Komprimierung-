import heapq
import numpy as np
import json 
from numpy.typing import NDArray

filename  = 'Huffman_tabelle.json'



class Node:
    def __init__(self, symbol=None, frequency=None, nodes= 1):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.nodes = nodes 
        
    def __lt__(self, other):

        if self.frequency == other.frequency:

            return self.nodes >= other.nodes
             
        else:
            return self.frequency < other.frequency
    
def calculate_frequencys( data : NDArray[np.int16]) -> NDArray[np.uint16]:
   
   bins = np.arange(-32768,32769)

   hist  : NDArray[np.int16]
   
   hist ,_= np.histogram(data,bins)


   

   return hist



def generate_huffmantree( frequencys : NDArray[np.int16]) -> Node:
    heap = []
    test = len(frequencys)
    for i in range(0,len(frequencys)):
        value = i - 32678

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
    """ Generierung der 

    Args:
        node (Node): _description_

    Returns:
        dict[int, str]: _description_
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
    return codetable

   

   

def write_table_to_file(codetable : dict[int,str]) -> None:

  
     with open(filename, 'w') as f:
         json.dump(codetable, f)




    


    