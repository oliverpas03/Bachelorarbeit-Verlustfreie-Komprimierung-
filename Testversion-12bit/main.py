import pandas as pd
import numpy as np 
from numpy.typing import NDArray
import csv

import huffman as huff
import decoder as dec 
import encoder as enc 
import sys

data_filename = 'Data/LOG10202.TXT'

def compression_ratio(originaldaten , codierte_daten):
    """_summary_: Berechnung von Komressionsrate

        Args:
            originaldaten (_type_): Eine numpy array Zeile der originalen Daten
            codierte_daten (string): Zeile in kodierter Form als String

        Returns:
            _type_: _description_
    """
    return (len(originaldaten)* 16)/ (len(codierte_daten)*8)
def remove_uneccesary_data( data) -> NDArray[np.int16]:
    """_summary_: Bereinigung der Daten und Umwandlung in numpy Array


        Args:
            data (): Originaldaten als pandas Datenrahmen

        Returns:
            NDArray[np.int16]: bereinigte Daten als numpy Array
        """
    data = data[data.iloc[:, 0] != 'GPS']
    data = data.iloc[:, 5:]
    data = data.reset_index(drop=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    data = data.fillna(0)
    array = data.to_numpy(dtype=np.int32)
    array_int = data.values.astype(np.int16)

    return array_int



def split_data( data: NDArray[np.int16])-> tuple[NDArray[np.uint8], NDArray[np.uint16]]:
    """ Die Funktion trennt das eingegebene Array in zwei verschiedene Arrays auf.
        Das eine enthält die vorderen vier bit

    :param data: Numpy Array das die Deltas der Datei enthält
    :return: Ein Array das die höchsten vier Bit enthält und eines das die restlichen 12 Bit enthält
    """




    four_bit = ((data >> 12) & 0x000F).astype(np.uint8)
    twelve_bit = (data & 0x0FFF).astype(np.uint16)

    return four_bit, twelve_bit

if __name__ == "__main__":
  
 
    
    
    
    # Erstelle Test-Datei
    with open('test_sensor.csv', 'w', encoding='utf-8') as f:
        f.write("""ACC,3890794474,10202,18.04.2023,08:14:34,-32768,32767,32767,-10000,2261,-550,-8678,2275,-110,-8551,2012,-348,-8211,296,767,-7622,-1774,2124,-6800,-2526,1343,-5542,-2067,845,-5936,-1842,83,-5208,-4476,-128,-7001,-3784,1004,-7966,-3819,-359,-7739,-23352,4377,-15542,16702,-20274,-28443,-807,2352,-3144,1028,-78,-8086,4109,-2412,-7921,3506,-249,-8096,2867,-616,-7887,2027,-280,-8112
                ACC,3890795013,10202,18.04.2023,08:23:33,2808,-7388,-1769,2351,-7460,-1613,2275,-7522,-2104,2981,-7631,-1657,3827,-6816,-2580,3901,-7795,-2559,4284,-6823,-2753,3817,-7296,-2035,4299,-6793,-1614,4057,-6686,-1798,4085,-6946,-1752,4617,-6457,-1799,4582,-6648,-1353,4316,-6606,-1646,4722,-6464,-1587,4285,-6777,-2738,4848,-6532,-2009,4223,-6929,-2158,3924,-6693,-2354,4549,-6504,-1602""")

    
    
    lines = []
    with open(data_filename, 'r') as f:
       for line in f:
          if not line.startswith('GPS'):
            lines.append(line.strip().split(','))


    data = pd.DataFrame(lines)

 
  
    
    

    data_array = remove_uneccesary_data(data) # Array mit den Daten
    original_daten = data_array.copy()



    differences = enc.calculate_differences(data_array) #Array der Deltas 
    array_4bit,array_12bit  = split_data(differences)

    frequencys_4bit = huff.calculate_frequencys(array_4bit)
    frequencys_12bit =huff.calculate_frequencys(array_12bit)
   

    huffman_tree_12bit = huff.generate_huffmantree( frequencys_12bit)
    huffman_tree_4bit = huff.generate_huffmantree(frequencys_4bit)

    codetable_12bit   = huff.generate_codes(huffman_tree_12bit, "twelwe_bit")
    codetable_4bit = huff.generate_codes(huffman_tree_4bit, "four_bit")
    codetable = (codetable_4bit,codetable_12bit)
    ratios = []
    overflowErrors = 0 
    for i in range(len(data_array)):
        #Eine Zeile Kodieren. Aktuell schon mit berecheten Deltas aus Geschwindikeitsgründen
        encoded_line, padding = enc.encode_line(differences[i], codetable_4bit,codetable_12bit)
        decoded_line = dec.decode(encoded_line,padding, huffman_tree_4bit,huffman_tree_12bit)
        ratios.append(compression_ratio(original_daten[i], encoded_line))
       
        if np.array_equal(original_daten[i], decoded_line) == False:
          overflowErrors += 1
    
    print( "Kompressionsrate: " +str(np.mean(ratios)))
    print( "Fehler: "+str(overflowErrors))
           
           


   
