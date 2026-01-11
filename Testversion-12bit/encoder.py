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
            array[i] = data[i] - data[i-3]
    else:
          array[:, 3:] = array[:, 3:] - array[:, :-3]
    return array






def encode_line( line :NDArray[np.int16], codetable_4bit : NDArray[np.void] = None,codetable_12bit : NDArray[np.void] = None) -> tuple[bytearray, np.uint8]:
    """Kodierung einer Zeile

    Args:
        line (NDArray[np.int16]): Eindimensionales Array mit Messwerten
        codetable (dict[int , str], optional): Codetabelle. Bennötig noch Funktionalität das sie aus Datei eingelesen werden kann falls nicht verhanden 

    Returns:
        str: Kodierte NAchricht
    """

    #differences = calculate_differences_one_line(line)


    front_4_bit = ((line >> 12)& 0x000F).astype(np.uint8)
    back_12_bit = (line & 0x0FFF).astype(np.uint16)
 
    encoded_line = bytearray()
    
    buffer   = 0 
    position = 0 
    
    for i in range( len(line)):
        
        front = front_4_bit[i]
        back = back_12_bit[i]
       
        
      
        code_front = int(codetable_4bit[0][front])
        length_front = int(codetable_4bit[1][front]) 
      
       
        buffer  = (buffer << length_front) | code_front 
        position += length_front 
        
        
        while position >= 8:
            shift = position - 8 
            # Das oberste (älteste) Byte extrahieren
            byte = (buffer >> shift) & 0xFF
            encoded_line.append(byte)
            
            # Das geschriebene Byte aus dem Buffer löschen
            
            buffer &= (1 << shift) - 1 
            position -= 8 
        
        
        code_back = int(codetable_12bit[0][back])
        length_back = int(codetable_12bit[1][back])
      
       
        buffer = (buffer << length_back) | code_back 
        position += length_back 

        while position >= 8:
            shift = position - 8 
            # Das oberste (älteste) Byte extrahieren
            byte = (buffer >> shift) & 0xFF
            encoded_line.append(byte)
            
            # Das geschriebene Byte aus dem Buffer löschen
            
            buffer &= (1 << shift) - 1 
            position -= 8 


    # Padding für das letzte Byte
    padding = 0
    if position > 0:
        padding = 8 - position
        # Restliche Bits nach links schieben
        byte = (buffer << padding) & 0xFF
        encoded_line.append(byte)

    return encoded_line, np.uint8(padding)



