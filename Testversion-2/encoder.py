def calculate_differences( array ):
    
       for i in range(3,len(array)):
           array[i] = array[i] - array[i-3]

def calculate_differences2(array):
    if array.ndim == 1:
        # 1D Array
        for i in range(3, len(array)):
            array[i] = array[i] - array[i-3]
    else:
          array[:, 3:] = array[:, 3:] - array[:, :-3]
    return array



def encode_line( line , codetable : dict[int , str]) -> str:
    encoded_line = ''
    for value in line:
        encoded_line = encoded_line + codetable[value]
    return encoded_line
