import os
from machine import Pin, SoftSPI, I2C
from sdcard import SDCard
from pca9685 import PCA9685
from servo import Servos
import time
import network
import socket
import json
import _thread

requested_song = None


servos = None
servos_connected = [True, True, True, True, True, True, True, True,
                    True, True, True, True, True, True, True, True]

servos_angle = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

servo_number_side_switch = 9

internet_controllable_mode = True

lock = _thread.allocate_lock()

external_controlled_mode = False
main_controlled_mode = True

def external_mode_thread():
    global external_controlled_mode
    global main_controlled_mode
    global requested_song
    external_controlled_mode = False

    # Connect to Wi-Fi (if needed)
    ssid = 'WIFI SSID'
    password = 'WIFI PASSWORD'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    print("Connecting...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    
    print('Connected to Wi-Fi:', wlan.ifconfig())

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 44444))

    while True:
        data,addr = sock.recvfrom(128)  # Buffer size is 128 bytes
        print("Received data:", data, "from", addr)

        if data.strip() == b"Connect":
            sock.sendto(b"Attempting Connection", addr)
            external_controlled_mode = True
            while main_controlled_mode:
                sock.sendto(b"Waiting on main thread to stop", addr)
                print("Waiting for main to take park...")
                time.sleep(2)
                
                
            sock.sendto(b"Finished", addr)
            
            while external_controlled_mode:
                print("External control mode active")
                data,addr = sock.recvfrom(128)  # Buffer size is 128 bytes
                try:
                    value = int(data.decode().strip())
                    print("Got an int:", value)
                    pluck_servo(value)
                except ValueError:
                    if data.strip() == b"Disconnect":
                        main_controlled_mode = True
                        external_controlled_mode = False
                        break
                    elif data.strip() == b"save_song":
                        print("here1")
                        sock.sendto(b"send", addr)
                        
                        print("here2")
                        data,addr = sock.recvfrom(1028)
                        print("here3")
                        song_data = json.loads(data.decode())

                        # Write to file on SD card
                        print("Type:", type(song_data))  # should say <class 'dict'>

                        print("saving song: " + str(song_data["metadata"]["title"]))
                        with open("/sd/songs/" + str(song_data["metadata"]["title"]) + ".json", "w") as f:
                            f.write(json.dumps(song_data))

                    elif data.strip() == b"get_songs":
                        print("Sending list of songs")
                        songs = os.listdir('/sd/songs')
                        sock.sendto(json.dumps(songs).encode(), addr)
                        
                    elif data.strip() == b"play_song":
                        print("Selecting song")
                        data, addr = sock.recvfrom(128)
                        requested_song = data.decode().strip()
                        print("Requested song:", requested_song)
                        # Check if the song exists
                        if requested_song in os.listdir('/sd/songs'):
                            print("Playing song:", requested_song)
                            sock.sendto(b"Song found, playing", addr)
                            # We want the main thread to play the song
                            main_controlled_mode = True
                            external_controlled_mode = False
                            break

                        else:
                            print("Song not found:", requested_song)
                            sock.sendto(b"Song not found", addr)
                            
                    elif data.strip() == b"Clear_song":
                        requested_song = None
                        
                   
                



# =============================================# 
# Song Player
# =============================================
def song_player(song_name):
    # read in the song in json format from /sd/songs/
    try:
        with open("/sd/songs/" + str(song_name), "r") as f:
            print("File exists!")
            song_data = json.loads(f.read())    

            print("Playing song:", song_data["metadata"]["title"])
            for note in song_data["notes"]:
                pluck_servo(int(note["tine"]))
                time.sleep_ms(note["gap_duration"])
    except OSError:
        print("File not found.")


        
# =============================================
# SD Card Setup
# =============================================
def setup_sd_card():
    # Pin assignment for SD card (using hardware SPI)
    # MISO -> GPIO 19
    # MOSI -> GPIO 23
    # SCK  -> GPIO 18
    # CS   -> GPIO 5
    spisd = SoftSPI(-1, miso=Pin(19), mosi=Pin(23), sck=Pin(18))
    sd = SDCard(spisd, Pin(5))
    
    # Mount filesystem
    vfs = os.VfsFat(sd)
    os.mount(vfs, '/sd')
    print('SD Card mounted')
    print('SD Card contains:', os.listdir('/sd'))
    return sd

# =============================================
# Servo Controller Setup
# =============================================
def setup_servos():
    # I2C setup for PCA9685 servo controller
    i2c = I2C(sda=Pin(21), scl=Pin(22))
    pca = PCA9685(i2c=i2c)
    global servos
    servos = Servos(i2c=i2c)
    n = 16
    
    # Initialize all servos to starting position
    # Pluck all tines (move up)
    for i in range(n):
        if servos_connected[i]:
            if i < 9:
                servos_angle[i] = 110
                servos.position(index=i, degrees=110)
            else:
                servos_angle[i] = 110
                servos.position(index=i, degrees=70)
            time.sleep(0.5)
    
    print('Servos initialized')

def pluck_servo(index_to_pluck):
    if index_to_pluck < 9:
        if servos_angle[index_to_pluck] == 0:
            servos_angle[index_to_pluck] = 110
            servos.position(index=index_to_pluck, degrees=110)
        else:
            servos_angle[index_to_pluck] = 0
            servos.position(index=index_to_pluck, degrees=0)
    else:
        if servos_angle[index_to_pluck] == 180:
            servos_angle[index_to_pluck] = 70
            servos.position(index=index_to_pluck, degrees=70)
        else:
            servos_angle[index_to_pluck] = 180
            servos.position(index=index_to_pluck, degrees=180)






# =============================================
# Main Application
# =============================================
def main():
    # Initialize hardware
    #sd = setup_sd_card()
    global main_controlled_mode
    global external_controlled_mode
    global servos
    global requested_song
    
    setup_servos()
    sd = setup_sd_card()

    _thread.start_new_thread(external_mode_thread, ())

    while True:

        while not external_controlled_mode:
            if requested_song is None:
                print("Waiting for external control mode...")
                time.sleep(1)
            else:
                print(requested_song)
                song_player(requested_song)
                time.sleep(5)

        if external_controlled_mode:
            main_controlled_mode = False
            while not main_controlled_mode:
                print("Waiting for external mode to finish...")
                time.sleep(1)





if __name__ == '__main__':
    main()
    print("EXITING")