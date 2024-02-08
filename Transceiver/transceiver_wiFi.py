import sys
import argparse
import threading
import struct
from datetime import datetime
import time
import pigpio
import traceback
from nrf24 import *
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore



# Use a service account.
cred = credentials.Certificate('./weather-station-554c2-firebase-adminsdk-4vk5n-a1079c9cd4.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

interval_min = 60
is_toggle = 0

parser = argparse.ArgumentParser(description="Send data.")
parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to send to (3 to 5 ASCII characters).")
args = parser.parse_args()
hostname = args.hostname
port = args.port
address = args.address
pi = pigpio.pi(hostname, port)

if not (2 < len(address) < 6):
    print(f'Invalid address {address}. Addresses must be 3 to 5 ASCII characters.')
    sys.exit(1)

nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.LOW)

def toggle_settings(name):
    while True:
        toggle_from_cloud = db.collection("toggle-and-interval").document("is75spvg9bgjlcBTgX2a")
        doc = toggle_from_cloud.get()
        data_dict = doc.to_dict()
        global is_toggle, interval_min

        if doc.exists:
            print(f"Document data: toggle = {data_dict['toggle']} , interval = {data_dict['interval']}")
            
            is_toggle = data_dict['toggle']
            if (is_toggle == 1):
                interval_min = data_dict['interval']
                payload = struct.pack("<Bff", 0x02, 1, 1)
                 # Send the payload to the address specified above.
                nrf.reset_packages_lost()
                nrf.send(payload)

                
                try:
                    nrf.wait_until_sent()
                except TimeoutError:
                    print('Timeout waiting for transmission to complete.')
                    # Wait 10 seconds before sending the next reading.
                    # time.sleep(10)
                    continue
                
                if nrf.get_packages_lost() == 0:
                    print(f"Success: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
                else:
                    print(f"Error: lost={nrf.get_packages_lost()}, retries={nrf.get_retries()}")
                
                interval_min = time.sleep(interval_min * 60)


            else:
                print("No such document!")

            time.sleep(1)


tx_thread = threading.Thread(target=toggle_settings, args=(1,))
tx_thread.start()




def receive_data(name):
    try:
        print(f'Receive from {address}')
        count = 0
        
        data_buffer ={
            'temp':{
                'recorded': False,
                'value':0
            },
            'hum':{
                'recorded': False,
                'value':0
            },
            'soil':{
                'recorded': False,
                'value':0
            },
            'anemo':{
                'recorded': False,
                'value':0
            }
        }
        
        while True:
            # As long as data is ready for processing, process it.
            while nrf.data_ready():
                # Count message and record time of reception.            
                count += 1
                now = datetime.now()
                
                # Read pipe and payload for message.
                pipe = nrf.data_pipe()
                payload = nrf.get_payload()    

                # Resolve protocol number.
                protocol = payload[0] if len(payload) > 0 else -1            

                hex = ':'.join(f'{i:02x}' for i in payload)

                # Show message received as hex.
                print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}")

                # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                
                soil = 0
                anemo = 0
                humi = 0
                temp = 0

                
                if payload[0] == 0x03:
                    if payload[0] == 0x03:
                        values = struct.unpack("<BfB", payload)
                        print(f'Protocol: {values[0]}, soil: {values[1]}, anemo: {values[2]}')
 
                        soil = int(values[1])
                        anemo = values[2]
    
                        # Ubah nilai soil menjadi string sesuai keinginan
                        soil_status = "Kering" if soil == 1 else "Basah"
    
                        data_buffer['soil']['recorded'] = True
                        data_buffer['soil']['value'] = soil_status
                    
                        data_buffer['anemo']['recorded'] = True
                        data_buffer['anemo']['value'] = anemo
                    
                    
                if payload[0] == 0x04:
                    values = struct.unpack("<Bff", payload)
                    print(f'Protocol: {values[0]}, humidity: {values[1]}, temperature: {values[2]}')
                 
                    humi = values[1]
                    temp = values[2]
                    
                    data_buffer['hum']['recorded'] = True
                    data_buffer['hum']['value'] = humi
                    
                    data_buffer['temp']['recorded'] = True
                    data_buffer['temp']['value'] = temp
                    
                false_detected = False
                
                for d in data_buffer:
                    recorded_state = data_buffer[d]['recorded']
                        
                    if recorded_state == False:
                        false_detected = True
                
                mapped_buffer =list(map(lambda d: data_buffer[d]['recorded'], data_buffer))
                
                if false_detected:
                    print(f'Data still empty: {mapped_buffer}')
                else:
                    
                    converted_dict_firestore={}
                    
                    for d in data_buffer:
                        print(d)
                        converted_dict_firestore[d] = data_buffer[d]['value']

                    print('converted firestore=')
                    print(converted_dict_firestore)
                    
                    converted_dict_firestore['ts'] = datetime.now()

                    added = db.collection("weather_data").add(converted_dict_firestore)
                
                
                time.sleep(1)
                
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()

tx_thread1 = threading.Thread(target=receive_data, args=(1,))
tx_thread1.start()
