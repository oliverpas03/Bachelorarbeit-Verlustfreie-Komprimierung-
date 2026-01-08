import numpy as np
from numpy.typing import NDArray

def calculate_differences_one_line( array : NDArray[np.int16]) -> NDArray[np.int16]:
    """Berechnen von Deltas für ein Datenpacket bzw. eine Arrayzeile

    Args:
        array (NDArray[np.int16]): Array mit Messwerten

    Returns:
        NDArray[np.int16]: Array mit Deltas 
    """
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



def encode_line( line :NDArray[np.int16], codetable : dict[int , str] = None) -> str:
    """Kodierung einer Zeile

    Args:
        line (NDArray[np.int16]): Eindimensionales Array mit Messwerten
        codetable (dict[int , str], optional): Codetabelle. Bennötig noch Funktionalität das sie aus Datei eingelesen werden kann falls nicht verhanden 

    Returns:
        str: Kodierte NAchricht
    """

    #differences = calculate_differences_one_line(line)
    encoded_line = ''
    for value in line:
        encoded_line = encoded_line + codetable[int(value)]
    return encoded_line



