import numpy as np
from numpy.typing import NDArray

def calculate_differences_one_line( array : NDArray[np.int16]) -> NDArray[np.int16]:
       new_array = array.copy()
    
       for i in range(3,len(array)):
           difference = array[i] -array[i-3]
           new_array[i]=  array[i] - array[i-3]
       return new_array

def calculate_differences(data : NDArray[np.int16]) -> NDArray[np.int16]:
    """Berechnung der Deltas für eine ganze Datei

     Args:
        array (NDArray[np.int16]): Array mit den Messwerten der ganzen Datei

     Returns:
        NDArray[np.int16]: Array mit den Deltas
    """
    array = data.copy()
    if array.ndim == 1:
        # 1D Array
        for i in range(3, len(array)):
            array[i] = array[i] - array[i-3]
    else:
          array[:, 3:] = array[:, 3:] - array[:, :-3]
    return array



def encode_line( line :NDArray[np.int16], codetable_4bit: dict[int , str],codetable_12bit : dict[int , str] = None) -> str:
    """

    :param line:  Arrayzeile welche die zu kodierenden Daten enthält.
    :param codetable_4bit:
    :param codetable_12bit:
    :return: Kodierte Zeile als Bitstring
    """

    #differences = calculate_differences_one_line(line)

    encoded_line = ''
    front_4_bit = ((line >> 12)& 0x000F).astype(np.uint8)
    back_12_bit = (line & 0x0FFF).astype(np.uint16)
    for i in range(0,len(line)):

        encoded_line = encoded_line + codetable_4bit[front_4_bit[i]]+codetable_12bit[back_12_bit[i]]

    

    
    return encoded_line



