import heapq
import numpy as np
import json
from numpy.typing import NDArray

EOF = 17 

codetable_file_4bit = 'codetable_4bit.bin'
codelengths_file_4bit = 'codelength_4bit.bin'

codetable_file_12bit = 'codetable_12bit.bin'
codelengths_file_12bit = 'codelength_12bit.bin'

class Node:
    def __init__(self, symbol=None, frequency=None, nodes= 1):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.nodes = nodes 
        
    def __lt__(self, other):

        if self.frequency != other.frequency:

            return self.frequency < other.frequency
             
        else:
            return self.nodes < other.nodes

    
def calculate_frequencys( data ) -> NDArray[np.uint16]:
    """Berechnung der Vorkommen der Werte für beide Teile (Vier und 12 Bit)

    Args:
        data (NDArray[int]): Array mit Werten deren Häufigkeit bestimmt werden muss

    Returns:
        NDArray[np.uint16]: Array mit Häufigkeiten entweder für Vier oder Zwölf Bit
    """
    bins = []
    if data.dtype == np.uint16:
       bins = np.arange(0,4097)
    if data.dtype == np.uint8:
       bins = np.arange(0,18)



   
    hist ,_= np.histogram(data,bins)


    

    return hist



def generate_huffmantree( frequencys : NDArray[np.int16]) -> Node:
    """ Erstellen von Huffman Baum aus Häufikeitstabelle

    Args:
        frequencys (NDArray[int]): _description_

    Returns:
        Node: _description_
    """

    heap = []
    test = len(frequencys)
    for i in range(0,len(frequencys)):

        node = Node( symbol= i, frequency = frequencys[i])
        heap.append( node)
    heapq.heapify(heap)
    while( len(heap ) > 1):
        smallest_frequency = heapq.heappop(heap)
        second_smallest_frequency = heapq.heappop(heap)

        new_node = Node( frequency= smallest_frequency.frequency + second_smallest_frequency.frequency , nodes = 1+ smallest_frequency.nodes +second_smallest_frequency.nodes)

        new_node.left = smallest_frequency
        new_node.right = second_smallest_frequency

        heapq.heappush(heap, new_node)
    #write_tree_to_file(heap[0])
    return heap[0]


def generate_codes(node: Node, type :str ) -> tuple[NDArray[int], NDArray[np.uint8] ]:
    """ Generierung der Codetabelle aus dem Baum.

    Args:
        node (Node): Wurzel des Huffman Baumes

    Returns:
        dict[int, str]: Codetabelle als zwei arrays 

    """
    if type == 'four_bit':

       
        codetable = np.zeros(17, dtype=np.uint16)
        codelengths = np.zeros(17, dtype = np.uint8)
    else: 
        
        codetable = np.zeros(4096, dtype=np.uint32)
        codelengths = np.zeros(4096, dtype = np.uint8)

  
    
    if node is None:
        return codetable
    
   
    stack = [(node, 0, 0)]
    
    while stack:
        current_node, code , length= stack.pop()
        
        if current_node is not None:
            # Blatt gefunden (Symbol vorhanden)
            if current_node.symbol is not None:
                index = current_node.symbol 
                codetable[index] = code
                codelengths[index] = length
            
            # Rechts zuerst auf Stack (wird später verarbeitet)
            if current_node.right is not None:
                new_code = ( code << 1) | 1 
                stack.append((current_node.right, new_code, length +1 ))
            
            # Links danach (wird zuerst verarbeitet - DFS)
            if current_node.left is not None:
                new_code = (code << 1) | 0
                stack.append((current_node.left, new_code, length +1 ))
    
    write_table_to_file(codetable,codelengths,type)
  
    return codetable,codelengths

   

def write_table_to_file(codetable : NDArray[np.uint64],lengths :NDArray[np.uint8],type = str) -> None:
    """Schreibt die beiden arrays in einzelne dateien 

    Args:
        codetable (NDArray[np.uint64]): _description_
        lengths (NDArray[np.uint8]): _description_
    """

    if type == "four_bit":
        codetable.tofile(codetable_file_4bit)
        lengths.tofile(codelengths_file_4bit)
    else:
        codetable.tofile(codetable_file_12bit)
        lengths.tofile(codelengths_file_12bit)

    



def write_tree_to_file( tree : Node )-> None: 
    """ Baum als Array in Datei schreiben. Muss noch geändert werden. Wird viel zu groß

    Args:
        tree (Node): _description_
    """
    array = np.zeros(tree.nodes, dtype= np.int32)
    stack = [ (tree,0)]

    while stack != []:

        node, index = stack.pop()
        
        if node is not None:
           
            if node.symbol is not None:
              array[index]= node.symbol
           
            if node.right is not None:
                array[index ] = -1 
                stack.append((node.right, 2*index+2 ))
            
           
            if node.left is not None:
                array[index]= -1
                stack.append( (node.left, 2*index+1))

    array.tofile('huffmantree.bin')


    


