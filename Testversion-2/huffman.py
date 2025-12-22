import heapq

class Node:
    def __init__(self, symbol=None, frequency=None, parent=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
        self.parent = parent
    def __lt__(self, other):
        return self.frequency < other.frequency
    
def determine_frequency(array) -> dict[int,int]:
    frequencys = {}
    if array.ndim == 1:
        # 1D Array
         for value in array:
            if value in frequencys.keys():
                frequencys[int(value)] += 1
            else: 
                frequencys.update( {int(value) : 1})
    else:

         for row in array:
              for value in row:
                 if value in frequencys.keys():
                    frequencys[int(value)] += 1
                 else: 
                    frequencys.update( {int(value) : 1})
    return frequencys
def generate_codes(node, code, codetable):
       if node is not None:
            if node.symbol is not None:
               codetable[node.symbol] = code
            generate_codes(node.left, code + [0], codetable)
            generate_codes(node.right, code + [1], codetable)
       return codetable

def generate_huffmantree( frequencys : dict[int,int]) -> Node:
    heap = []
    for value in frequencys.keys(): 
        node = Node( symbol= value, frequency = frequencys[value])
        heap.append( node)
    heapq.heapify(heap)
    while( len(heap ) > 1):
        smallest_frequency = heapq.heappop(heap)
        second_smallest_frequency = heapq.heappop(heap)

        new_node = Node( frequency= smallest_frequency.frequency + second_smallest_frequency.frequency )

        new_node.left = smallest_frequency
        new_node.right = second_smallest_frequency

        heapq.heappush(heap, new_node)
    return heap[0]


def generate_codes(node, code , codetable):
    if node is not None:
        if node.symbol is not None:
            codetable[node.symbol] = code
        generate_codes(node.left, code + '0', codetable)
        generate_codes(node.right, code + '1', codetable)
    return codetable



    