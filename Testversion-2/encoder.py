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
            array[i] = data[i] - data[i-3]
    else:
          array[:, 3:] = array[:, 3:] - array[:, :-3]
    return array



def encode_line( line :NDArray[np.int16], codetable : NDArray[np.void] = None) -> tuple[bytearray, np.uint8]:
    """Kodierung einer Zeile

    Args:
        line (NDArray[np.int16]): Eindimensionales Array mit Messwerten
        codetable (dict[int , str], optional): Codetabelle. Bennötig noch Funktionalität das sie aus Datei eingelesen werden kann falls nicht verhanden 

    Returns:
        str: Kodierte NAchricht
    """

    #differences = calculate_differences_one_line(line)
 
    encoded_line = bytearray()
    
    buffer = 0 
    position = 0 
    
    for value in line:
        # Index-Berechnung für int16
        index = np.uint16(np.int32(value) + 32768)
        
      
        code = int(codetable[0][index])
        length = int(codetable[1][index])
      
        # Code in den Buffer schieben
        buffer = (buffer << length) | code 
        position += length 
        
        # Sobald wir mindestens ein Byte (8 Bit) zusammen haben
        while position >= 8:
            shift = position - 8 
            # Das oberste (älteste) Byte extrahieren
            byte = (buffer >> shift) & 0xFF
            encoded_line.append(byte)
            
            # Das geschriebene Byte aus dem Buffer löschen
            # (1 << shift) - 1 erzeugt eine Maske für die verbleibenden Bits
            buffer &= (1 << shift) - 1 
            position -= 8 

    # Padding für das letzte Byte
    padding = 0
    if position > 0:
        padding = 8 - position
        # Restliche Bits nach links schieben (MSB-Ausrichtung)
        byte = (buffer << padding) & 0xFF
        encoded_line.append(byte)

    return encoded_line, np.uint8(padding)


