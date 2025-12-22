import numpy as np
from numpy.typing import NDArray

def calculate_differences( array : NDArray[np.int16]) -> NDArray[np.int16]:
       new_array = array.copy()
    
       for i in range(3,len(array)):
           difference = array[i] -array[i-3]
           new_array[i]=  array[i] - array[i-3]
       return new_array

def calculate_differences2(array : NDArray[np.int16]) -> NDArray[np.int16]:
    if array.ndim == 1:
        # 1D Array
        for i in range(3, len(array)):
            array[i] = array[i] - array[i-3]
    else:
          array[:, 3:] = array[:, 3:] - array[:, :-3]
    return array



def encode_line( line :NDArray[np.int16], codetable : dict[int , str] = None) -> str:

    differences = calculate_differences(line)
    encoded_line = ''
    for value in differences:
        encoded_line = encoded_line + codetable[value]
    return encoded_line
