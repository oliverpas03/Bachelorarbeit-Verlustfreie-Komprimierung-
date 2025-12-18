import csv
import dynamc_huffman as huff

def normalise_date(date):
    day, month , year = date.split('.')
    return  int(year + month + day)
def normalise_time(time):
    hour, minute , second = time.split(':')
    return  int(hour+minute +second) 

def denormalize_date(date):
    year,month,day = date[:4], date[4:6], date[6:8]
    return day+"."+month+"."+year

def denormalise_time(time):
    if len(time) < 6: 
        time = "0"+time
    hour, minute , second = time[:2], time[2:4] , time[4:6]
    return hour + ":"+minute+":"+second
class DeltaEncoder:
    
    
    def __init__(self):
        self.prev_GPS_data = {}
        self.prev_ACC_data = {}
        self.code = huff.Huffman_Code()
    
    def encode_line(self, line):
        """Kodiert eine Zeile zu Bit-String - ZWEI PHASEN"""
        if line is None:
            return None
        
        # Typ-Bit: Anstatt ACC oder GPS auch zu kodieren habe ich einfach festgelegt das sie jeweils den wet 0 oder eins haben
        type_bit = 0 if line[0] == "ACC" else 1
        
        # Datum/Zeit normalisieren
        date = normalise_date(line[3])
        time = normalise_time(line[4])
        
        # Vorherige Daten wählen
        prev_data = self.prev_ACC_data if type_bit == 0 else self.prev_GPS_data
        
        # Differenzen berechnen
        differences = []
        differences.append(int(line[1]) - prev_data.get('id', 0))
        differences.append(int(line[2]) - prev_data.get('code', 0))
        differences.append(date - prev_data.get('date', 0))
        differences.append(time - prev_data.get('time', 0))
        
        for i in range(5, len(line)):
            if line[i] == '-':
                current_val = 0
            else:
                try:
                    current_val = int(line[i])
                except ValueError:
                    current_val = ord(line[i])
            
            prev_val = prev_data.get(f'value_{i}', 0)
            differences.append(current_val - prev_val)
        
        # PHASE 1: TRAINING
        for diff in differences:
            diff_str = str(diff)
            huff.huffman_encode(self.code, diff_str)
        
        # PHASE 2: ENCODING
        bit_string = str(type_bit)  # Start mit Typ-Bit
        for diff in differences:
            diff_str = str(diff)
            code_bits = self.code.codes[diff_str]
            bit_string += ''.join(map(str, code_bits))
        
        # Update Zustand
        new_prev_data = {
            'id': int(line[1]),
            'code': int(line[2]),
            'date': date,
            'time': time
        }
        for i in range(5, len(line)):
            if line[i] == '-':
                new_prev_data[f'value_{i}'] = 0
            else:
                try:
                    new_prev_data[f'value_{i}'] = int(line[i])
                except ValueError:
                    new_prev_data[f'value_{i}'] = ord(line[i])
        
        if type_bit == 0:
            self.prev_ACC_data = new_prev_data
        else:
            self.prev_GPS_data = new_prev_data
        
        return bit_string
    

class DeltaDecoder:
    def __init__(self):
        self.prev_GPS_data = {}
        self.prev_ACC_data = {}
        self.code = huff.Huffman_Code()

    def decode_line(self, bit_string):
        type_bit , encoded_data = bit_string[0], bit_string[1:]
        differences = huff.huffman_decode(self.code, encoded_data)

        reconstructed_line = []
        prev_data = {}

        if type_bit == "0":
            reconstructed_line.append("ACC")
            prev_data = self.prev_ACC_data
        else:
            reconstructed_line.append("GPS")
            prev_data = self.prev_GPS_data

        
        id = prev_data.get("id",0) + int(differences[0])
        reconstructed_line.append(id)

        code = prev_data.get("code", 0) +int( differences[1])
        reconstructed_line.append(code)

        date = prev_data.get("date",0) +int(differences[2])
        reconstructed_line.append(denormalize_date(str(date)))

        time = prev_data.get("time",0) +int( differences[3])
        reconstructed_line.append( denormalise_time(str(time)))

        
        values = []
        for i in range(  len(differences)-4):
            values.append(prev_data.get( f"value{i}", 0) +int(differences[i+4]))
            reconstructed_line.append(values[i])


        new_prev_data = {
            'id': id,
            'code': code,
            'date': date,
            'time': time
        }
        for i in range(len(values)):
            
                try:
                    new_prev_data[f'value_{i}'] = int(values[i])
                except ValueError:
                    new_prev_data[f'value_{i}'] = ord(values[i])
        
        if type_bit == "0":
            self.prev_ACC_data = new_prev_data
        else:
            self.prev_GPS_data = new_prev_data

        return reconstructed_line
    
if __name__ == "__main__":
  
   
    
    
    
    # Erstelle Test-Datei
    with open('test_sensor.csv', 'w', encoding='utf-8') as f:
        f.write("""ACC,3890794375,10211,18.04.2023,08:12:55,-7417,2960,796
ACC,3890794376,10211,18.04.2023,08:12:56,-6438,4625,-271
GPS,3890794210,10211,18.04.2023,08:10:10,0,0,0,1,B,-1
ACC,3890794210,10211,18.04.2023,08:10:10,-6454,2930,-2860
GPS,3890794211,10211,18.04.2023,08:10:11,0,0,0,1,B,-1""")
    
    print("\nKodiere erste Zeile mit ZWEI PHASEN:")
    print("-"*70)
    
    encoder = DeltaEncoder()
    decoder = DeltaDecoder()

    decoder.code = encoder.code 
    
    with open('test_sensor.csv', 'r') as f:

        csv_reader = csv.reader(f)
        for line_num, line in enumerate(csv_reader, 1):
            print(f"\nZeile {line_num}: {line}")
            
            result = encoder.encode_line(line)
           
      
       

        

            print(result)

            decoded_result = decoder.decode_line(result)

            print(decoded_result)
    

        
        
        


            





