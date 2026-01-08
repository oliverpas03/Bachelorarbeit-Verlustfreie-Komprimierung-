import pandas as pd
import numpy as np 
from numpy.typing import NDArray
import csv

import huffman as huff
import decoder as dec 
import encoder as enc 


data_filename = 'Data/LOG10202.txt'


    
    
"""_summary_

    Args:
        originaldaten (_type_): Eine numpy array Zeile der originalen Daten
        codierte_daten (string): Zeile in kodierter Form als String

    Returns:
        _type_: _description_
""" 
def compression_ratio(originaldaten , codierte_daten):
   
   return (len(originaldaten)* 16)/ len(codierte_daten)
def remove_uneccesary_data( data) -> NDArray[np.int16]:
    """_summary_: Bereinigung der Daten und Umwandlung in numpy Array
                  

    Args:
        data (_type_): Originaldaten als pandas Datenrahmen

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

if __name__ == "__main__":
  
 
    
    
    
    # Erstelle Test-Datei
    with open('test_sensor.csv', 'w', encoding='utf-8') as f:
        f.write("""ACC,3890794474,10202,18.04.2023,08:14:34,-32768,32767,0,2261,-550,-8678,2275,-110,-8551,2012,-348,-8211,296,767,-7622,-1774,2124,-6800,-2526,1343,-5542,-2067,845,-5936,-1842,83,-5208,-4476,-128,-7001,-3784,1004,-7966,-3819,-359,-7739,-23352,4377,-15542,16702,-20274,-28443,-807,2352,-3144,1028,-78,-8086,4109,-2412,-7921,3506,-249,-8096,2867,-616,-7887,2027,-280,-8112
                ACC,3890795013,10202,18.04.2023,08:23:33,2808,-7388,-1769,2351,-7460,-1613,2275,-7522,-2104,2981,-7631,-1657,3827,-6816,-2580,3901,-7795,-2559,4284,-6823,-2753,3817,-7296,-2035,4299,-6793,-1614,4057,-6686,-1798,4085,-6946,-1752,4617,-6457,-1799,4582,-6648,-1353,4316,-6606,-1646,4722,-6464,-1587,4285,-6777,-2738,4848,-6532,-2009,4223,-6929,-2158,3924,-6693,-2354,4549,-6504,-1602""")

    
    
    lines = []
    with open(data_filename, 'r') as f:
       for line in f:
          if not line.startswith('GPS'):
            lines.append(line.strip().split(','))


    data = pd.DataFrame(lines)

 
  
    
    

    data_array = remove_uneccesary_data(data)
    original_daten = data_array.copy()



    differences = enc.calculate_differences(data_array)
    frequencys = huff.calculate_frequencys(differences)
   

    huffman_tree = huff.generate_huffmantree( frequencys)

    codetable : dict[int, str]  = huff.generate_codes(huffman_tree)
    ratios = []
    overflowErrors = 0 
    for i in range(len(data_array)):

        encoded_line = enc.encode_line(data_array[i], codetable)
        decoded_line = dec.decode(encoded_line,huffman_tree)
        ratios.append(compression_ratio(original_daten[i], encoded_line))
       
        if np.array_equal(original_daten[i], decoded_line) == False:
          overflowErrors += 1
    
    print( "Kompressionsrate: " +str(np.mean(ratios)))
    print( "Fehler: "+str(overflowErrors))
           
           


   
