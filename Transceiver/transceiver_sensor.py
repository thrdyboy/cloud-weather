import argparse
from datetime import datetime
import struct
import sys
import time
import traceback


import pigpio
from nrf24 import *
import Adafruit_DHT
from math import pi
import math

Pin_soil = 21

pi = pigpio.pi()  # Connect to local Pi's pigpio daemon
pi.set_mode(Pin_soil, pigpio.INPUT)  # Set pin as input

# rain_count = 0
# bucket_size = 0.7
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17  # Change this to the GPIO pin you are using (e.g., 4)
ANEMOMETER_PIN = 6  # Ganti dengan nomor pin GPIO yang Anda gunakan

def read_wind_data():
    pi = pigpio.pi()
    ANEMOMETER_PIN = 6  # Ganti dengan nomor pin GPIO yang Anda gunakan

    # pi.set_mode(ANEMOMETER_PIN, pigpio.INPUT)
    # pi.set_pull_up_down(ANEMOMETER_PIN, pigpio.PUD_UP)
    # pi.callback(ANEMOMETER_PIN, pigpio.FALLING_EDGE, count_wind)

    wind_count = 0
    radius_m = 0.1  # Ganti dengan radius anemometer dalam cm
    interval = 10.0  # Waktu dalam detik untuk menghitung putaran
    calibration_value = 2.0  # Sesuaikan dengan nilai kalibrasi
    ms_to_kmh = 3.6  # Faktor konversi dari m/s ke km/h

    def calculate_speed(time_sec):
        # global wind_count
        circum_m = 2 * math.pi * radius_m
        rotations = wind_count / time_sec  # Karena setiap 2 putaran dihitung sebagai 1 putaran
        # distance_cm = circum_m * rotations
        # speed = (distance_cm / interval) * ms_to_kmh  # Konversi dari cm/s ke km/h
        # return speed
        velocity_ms = circum_m * rotations #m/s
        velocity_kmh = velocity_ms*ms_to_kmh #km/h
        return velocity_kmh * calibration_value

    def count_wind(channel, level, tick):
        # global wind_count
        nonlocal wind_count
        wind_count += 1

    pi.set_mode(ANEMOMETER_PIN, pigpio.INPUT)
    pi.set_pull_up_down(ANEMOMETER_PIN, pigpio.PUD_UP)
    pi.callback(ANEMOMETER_PIN, pigpio.FALLING_EDGE, count_wind)

    try:
        # while True:
        wind_count = 0
        time.sleep(interval)
        wind_speed = calculate_speed(time_sec=60)
        calibrated_speed = wind_speed * calibration_value
        # print(f"Kecepatan Angin: {calibrated_speed:.2f} km/h")
        
        return calibrated_speed
    except KeyboardInterrupt:
        return 0.0

def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        humidity = '{:.2f}'.format(humidity)
        temperature = '{:.2f}'.format(temperature)
        return humidity, temperature
    else:
        return None

def get_soil_value():
    soil_value = 0
    
    # Digital read

    res_read = pi.read(Pin_soil)

    print()
    print(f'Read pin soil {res_read}')
    print()

    if res_read == 0:  # Check for HIGH level (water detected)
        soil_value = "Basah"
        
    else:
        soil_value = "Kering"
            
    return soil_value

def get_anemo_value():
    anemo_value = 0
    
    # Read anemo
    calibrated_speed = read_wind_data()
    anemo_value = calibrated_speed
    
    print(f'anemo: {anemo_value} Km/h')
    
    return anemo_value

def get_temperature_value():
    temperature_value = 0
    
    result = read_dht22()
    if result:
        _, temp = result
        # print(f'Humidity: {hum}%')
        print(f'Temperature: {temp}°C')
        
        temperature_value=temp
    else:
        print('Failed to retrieve data from the sensor.')
    
    # Read temperature
    
    return temperature_value


def get_humidity_value():
    humidity_value = 0
    
    result = read_dht22()
    if result:
        hum, _ = result
        # print(f'Humidity: {hum}%')
        print(f'Humidity: {hum}RH')
        
        humidity_value=hum
    else:
        print('Failed to retrieve hum data from the sensor.')
    
    # Read temperature
    
    return humidity_value

if __name__ == "__main__":

    print("Python NRF24 Simple Receiver Example.")
    
    # Parse command line argument.
    parser = argparse.ArgumentParser(description="Receive toggle and interval data")
    parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
    parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
    parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    address = args.address

    # Verify that address is between 3 and 5 characters.
    if not (2 < len(address) < 6):
        print(f'Invalid address {address}. Addresses must be between 3 and 5 ASCII characters.')
        sys.exit(1)
    
    # Connect to pigpiod
    print(f'Connecting to GPIO daemon on {hostname}:{port} ...')
    pi = pigpio.pi(hostname, port)
    if not pi.connected:
        print("Not connected to Raspberry Pi ... goodbye.")
        sys.exit()

    # Create NRF24 object.
    # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
    nrf = NRF24(pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_250KBPS, pa_level=RF24_PA.MIN)
    nrf.set_address_bytes(len(address))

    # Listen on the address specified as parameter
    nrf.open_reading_pipe(RF24_RX_ADDR.P1, address)
    
    # Display the content of NRF24L01 device registers.
    nrf.show_registers()

    # Enter a loop receiving data on the address specified.
    try:
        print(f'Receive from {address}')
        count = 0
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
                if payload[0] == 0x02:
                    values = struct.unpack("<Bff", payload)
                    print(f'Acquire sensor command received.')
                
                    soil = get_soil_value()

                    anemo = get_anemo_value()
                                
                    humidity = get_humidity_value()
                    
                    temperature = get_temperature_value()
                    
                    
                    
                    print('hum=')
                    print(humidity)
                    
                    print('temp=')
                    print(temperature)
                    
                    
                    
                    # Step 1
                    # payload = struct.pack("<Bff", 0x03, soil, int(float(anemo)))
                    payload = struct.pack("<BfB", 0x03, 1.0 if soil == "Kering" else 0.0, int(float(anemo)))

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

                    
                    # Step 2
                    payload = struct.pack("<Bff", 0x04, int(float(humidity)), int(float(temperature)))
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
                        

                    
                
            # Sleep 100 ms.
            time.sleep(0.1)
    except:
        traceback.print_exc()
        nrf.power_down()
        pi.stop()
