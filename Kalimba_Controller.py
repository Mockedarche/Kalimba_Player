import time
from lib import display, userinput
from lib.hydra import config
import socket
import network
from array import array
from lib.hydra import beeper
import os
from lib.sdcard import mhsdcard
import sys
import math
import json
 
"""
NOTES

Colors are just a 16 bit color aka RGB565 meaning whatever passed just becomes this. For fine grain control use a binary representation like 0b1111100000000000

Must call DISPLAY.show() to actually have changes applied. Think of it as VRR where the display is only updated when a frame is complete meaning we can set up an entire frame
whatever time span we want since the frame buffer is only pushed when we call. 

"""
 
sd = mhsdcard.SDCard()
sd.mount()
 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ _CONSTANTS: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_MH_DISPLAY_HEIGHT = const(135)
_MH_DISPLAY_WIDTH = const(240)
_DISPLAY_WIDTH_HALF = const(_MH_DISPLAY_WIDTH // 2)

_CHAR_WIDTH = const(8)
_CHAR_WIDTH_HALF = const(_CHAR_WIDTH // 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ GLOBAL_OBJECTS: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# init object for accessing display
DISPLAY = display.Display(use_tiny_buf=True)

# object for accessing microhydra config (Delete if unneeded)
CONFIG = config.Config()

# object for reading keypresses (or other user input)
INPUT = userinput.UserInput()

demo_layout_mode = False
demo_mode = True

# Used to clear screen
CONFIG.palette[0] = 0
# Text notes
CONFIG.palette[1] = 65472
# Recording logo
CONFIG.palette[2] = 63488
# Top Label background
CONFIG.palette[3] = 12292
# Bottom Label background
CONFIG.palette[4] = 10565
# White text
CONFIG.palette[5] = 65535
# Text keys
CONFIG.palette[6] = 12222
# Play lines
CONFIG.palette[7] = 23211
# Green for connected
CONFIG.palette[8] = 2016
# Main menu style border
CONFIG.palette[9] = 10989

"""
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
CONFIG.palette[3] =
"""
how_many_notes_to_show = 11
notes_played = [''] * how_many_notes_to_show
keys_played = [''] * how_many_notes_to_show
reload_overlay_flag = False
update_play_graphics = True
connected_flag = False

sock = None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clear_frame():
    # clear framebuffer
    DISPLAY.fill(CONFIG.palette[0])


def player(sock, address, demo_mode):
    global reload_overlay_flag
    global update_play_graphics
    recording_notes_played = []
    reload_overlay_flag = True
    last_blinked_recording_logo = time.ticks_ms()
    recording_blink_flag = False
    recording_flag = False
    play_sound_flag = True
    
    
    time_to_play_ms = 500
    
    songs_path = "/sd/Kalimba/Songs"

    print(os.listdir(songs_path))

    
    if play_sound_flag:
        for i in range(17):

            play_sound(i, 50)
            time.sleep_ms(51)
            
    
    
    while True:
        player_layout(play_sound_flag)
        keys = INPUT.get_new_keys()
        # if there are keys, convert them to a string, and store for display
        if keys:
            
            print(keys)
            
            if "1" in keys:
                packet = "0"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("0", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(0, time_to_play_ms)
                
                notes_played[0] = "1"
                keys_played[0] = "1"
                update_play_graphics = True
                
            elif "2" in keys:
                packet = "1"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("1", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(1, time_to_play_ms)
                    
                notes_played[0] = "2"
                keys_played[0] = "2"
                update_play_graphics = True

                
            elif "3" in keys:
                packet = "2"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("2", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(3, time_to_play_ms)
                
                notes_played[0] = "4"
                keys_played[0] = "3"
                update_play_graphics = True

                
            elif "4" in keys:
                packet = "3"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("3", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(5, time_to_play_ms)
                
                notes_played[0] = "6"
                keys_played[0] = "4"
                update_play_graphics = True

                
            elif "5" in keys:
                packet = "4"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("4", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(7, time_to_play_ms)
                
                notes_played[0] = "1'"
                keys_played[0] = "5"
                update_play_graphics = True

                
            elif "7" in keys:
                packet = "9"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("9", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(2, time_to_play_ms)
                
                notes_played[0] = "3"
                keys_played[0] = "7"
                update_play_graphics = True

                
            elif "8" in keys:
                packet = "10"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("10", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(4, time_to_play_ms)
                
                notes_played[0] = "5"
                keys_played[0] = "8"
                update_play_graphics = True

                
            elif "9" in keys:
                packet = "11"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                    
                if recording_flag:
                    recording_notes_played.append(("11", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(6, time_to_play_ms)
                
                notes_played[0] = "7"
                keys_played[0] = "9"
                update_play_graphics = True

                
            elif "0" in keys:
                packet = "12"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("12", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(8, time_to_play_ms)
                
                notes_played[0] = "2'"
                keys_played[0] = "0"
                update_play_graphics = True

                
            elif "-" in keys:
                packet = "13"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("13", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(10, time_to_play_ms)
                
                notes_played[0] = "4'"
                keys_played[0] = "_"
                update_play_graphics = True

                
            elif "t" in keys:
                packet = "5"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("5", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(9, time_to_play_ms)
                
                notes_played[0] = "3'"
                keys_played[0] = "t"
                update_play_graphics = True

                
            elif "r" in keys:
                packet = "6"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("6", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(11, time_to_play_ms)
                
                notes_played[0] = "5'"
                keys_played[0] = "r"
                update_play_graphics = True

                
            elif "e" in keys:
                packet = "7"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("7", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(13, time_to_play_ms)
                
                notes_played[0] = "7'"
                keys_played[0] = "e"
                update_play_graphics = True

                
            elif "w" in keys:
                packet = "8"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("8", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(15, time_to_play_ms)
                
                notes_played[0] = "2'"
                keys_played[0] = "w"
                update_play_graphics = True

                
            elif "u" in keys:
                packet = "14"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("14", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(12, time_to_play_ms)
                
                notes_played[0] = "6'"
                keys_played[0] = "u"
                update_play_graphics = True

                
            elif "i" in keys:
                packet = "15"
                if not demo_mode:
                    sock.sendto(packet, address)
                    
                if recording_flag:
                    recording_notes_played.append(("15", time.ticks_ms()))
                if play_sound_flag:
                    play_sound(14, time_to_play_ms)
                
                notes_played[0] = "1''"
                keys_played[0] = "i"
                update_play_graphics = True

                
            elif "ENT" in keys:
                if recording_flag:
                    save_song(recording_notes_played, address)
                    recording_notes_played.clear()
                    reload_overlay_flag = True
                    update_play_graphics = True
                    
                recording_flag = not recording_flag
                
                if recording_flag == False:
                    DISPLAY.rect(0, 122, 240, 42, CONFIG.palette[4], fill = True)
                    recording_logo()
                    
            
            elif 'CTL' in keys:
                reload_overlay_flag = True
                update_play_graphics = True
                if recording_flag:
                    startup_layout("Exit recording mode")
                    time.sleep(2)
                    
                else:
                    
                    return
                    
            elif 'FN' in keys:
                play_sound_flag = not play_sound_flag
                reload_overlay_flag = True
                
                    
                
        
        if recording_flag:
            if (last_blinked_recording_logo + 700) < time.ticks_ms():
                if recording_blink_flag:
                    # Background buttom lip
                    DISPLAY.rect(80, 122, 240, 42, CONFIG.palette[4], fill = True)
                    recording_blink_flag = False
                else:
                    recording_logo()
                    reload_overlay_flag = True
                    recording_blink_flag = True
                    
                last_blinked_recording_logo = time.ticks_ms()
                    
        time.sleep_ms(2)





def player_layout(play_sound_flag):
    global reload_overlay_flag
    global update_play_graphics
    global notes_played
    global keys_played
    global how_many_notes_to_show
    
    if reload_overlay_flag:
                        
        # Kalimba title
        DISPLAY.rect(0, 0, 240, 15, CONFIG.palette[3], fill = True)
        DISPLAY.text("Kalimba Controller", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Kalimba Controller") // 2)), y = 10 // 3, color = CONFIG.palette[5])
        
        # Background 
        DISPLAY.rect(0, 15, 240, 42, CONFIG.palette[4], fill = True)
        # Background buttom lip
        DISPLAY.rect(0, 115, 240, 42, CONFIG.palette[4], fill = True)
        
        # Stuff for the notes and corresponding key to press
        key_note1 = "NOTE: 1 2 4 6 1'3 5 7 2'4'"
        button_to_press1 = "KEY: 1 2 3 4 5 7 8 9 0 _"
        key_note2 = "NOTE: 3'5'7'2''6'1''"
        button_to_press2 = " KEY: t r e w  u i  "
        DISPLAY.text(key_note1, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(key_note1) // 2)), y = 53 // 3, color = CONFIG.palette[1])
        DISPLAY.text(button_to_press1, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(button_to_press1) // 2)), y = 85 // 3, color = CONFIG.palette[6])
        DISPLAY.text(key_note2, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(key_note2) // 2)), y = 115 // 3, color = CONFIG.palette[1])
        DISPLAY.text(button_to_press2, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(button_to_press2) // 2)), y = 147 // 3, color = CONFIG.palette[6])
        
        # Lines to add seperators for keys and notes
        DISPLAY.hline(0, 26, 240, CONFIG.palette[5])
        DISPLAY.hline(0, 46, 240, CONFIG.palette[5])
        
        # Recording lines
        DISPLAY.hline(0, 57, 240, CONFIG.palette[2])
        DISPLAY.hline(0, 120, 240, CONFIG.palette[2])
        
        # Sound icon
        if play_sound_flag:
            DISPLAY.polygon(array("h", [0, 2, 2, 2, 4, 0, 4, 8, 2, 6, 0, 6]), x=3, y=3, color=CONFIG.palette[1], fill=True)
            DISPLAY.polygon(array("h", [5, 3, 6, 4, 5, 5]), x=4, y=3, color=CONFIG.palette[1], fill=True)
            DISPLAY.polygon(array("h", [6, 2, 7, 4, 6, 6]), x=5, y=3, color=CONFIG.palette[1], fill=True)
        
            DISPLAY.text("FN", x = 15, y=4, color=CONFIG.palette[1])
            
        else:
            DISPLAY.polygon(array("h", [0, 2, 2, 2, 4, 0, 4, 8, 2, 6, 0, 6]), x=3, y=3, color=CONFIG.palette[4], fill=True)
            DISPLAY.polygon(array("h", [5, 3, 6, 4, 5, 5]), x=4, y=3, color=CONFIG.palette[4], fill=True)
            DISPLAY.polygon(array("h", [6, 2, 7, 4, 6, 6]), x=5, y=3, color=CONFIG.palette[4], fill=True)
        
            DISPLAY.text("FN", x = 15, y=4, color=CONFIG.palette[4])
        
        recording_logo()
        
        reload_overlay_flag = False
    
    if update_play_graphics:
        print("updated play")
        # Background 
        DISPLAY.rect(0, 58, 240, 62, CONFIG.palette[4], fill = True)    
        
        # Recording lines
        DISPLAY.hline(0, 77, 240, CONFIG.palette[7])
        DISPLAY.hline(0, 100, 240, CONFIG.palette[7])
        
        for i in range(how_many_notes_to_show):
            DISPLAY.text(str(notes_played[i]), x=(_MH_DISPLAY_WIDTH // (how_many_notes_to_show)) * i, y=68, color=CONFIG.palette[1])
            DISPLAY.text(str(keys_played[i]), x=(_MH_DISPLAY_WIDTH // (how_many_notes_to_show)) * i, y=91, color=CONFIG.palette[1])
            
        notes_played.pop()
        notes_played.insert(0, '')
        keys_played.pop()
        keys_played.insert(0, '')
        update_play_graphics = False
        
    DISPLAY.show()
    
def recording_logo():
    
    DISPLAY.text("MENU:", 2, 124, color = CONFIG.palette[1])
    DISPLAY.text("CTL", 42, 124, color = CONFIG.palette[1])
        
    
    DISPLAY.ellipse(192, 127, 4, 4, CONFIG.palette[2], fill = True)
    DISPLAY.text("ENTER", x = 200, y = 124, color = CONFIG.palette[2])
    
    
def startup_layout(text):
    clear_frame()
    
    DISPLAY.rect(0, 0, _MH_DISPLAY_WIDTH, _MH_DISPLAY_HEIGHT, CONFIG.palette[4], fill = True)

    DISPLAY.text(text, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(text) // 2)), y = (_MH_DISPLAY_HEIGHT // 2) - 10, color = CONFIG.palette[1])
    
    DISPLAY.show()


#NOTE not blocking
def play_sound(index, time_in_ms):
    if index < 17:
    
        kalimba_notes = [
        'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
        'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
        'C6', 'D6', 'E6'
        ]
            #init the beeper!
        beep = beeper.Beeper()

        beep.play(
            # a tuple of strings containing notes to play. a nested tuple can be used to play multiple notes together.
            notes=(kalimba_notes[index]),
            # how long to play each note
            time_ms=time_in_ms,
            # an integer from 0-10 representing the volume of the playback. Default is 2, 0 is almost inaudible, 10 is loud.
            volume=10,
        )

def save_song(recording_notes_played, address):
    clear_frame()
    song_title = ""
    
    DISPLAY.fill(CONFIG.palette[4]) 
    
    
    DISPLAY.text("Song title", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Song title") // 2)), y = 20, color = CONFIG.palette[1])
    DISPLAY.text("Proceed: ENTER", x = 125, y =120, color = CONFIG.palette[1])

    DISPLAY.show()
    
    while True:
        keys = INPUT.get_new_keys()
        if keys:
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter in keys:
                    if len(song_title) < 22:
                        song_title += letter
                        break
            if 'BSPC' in keys:
                if len(song_title) > 0:
                    song_title = song_title[:-1]
                    
            if 'ENT' in keys:
                if len(song_title) > 0:
                    break
            
        DISPLAY.rect(10, 40, 220, 16, CONFIG.palette[7], fill = True)

        DISPLAY.text(song_title, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(song_title) // 2)), y = 44, color = CONFIG.palette[1])
        DISPLAY.show()
        time.sleep_ms(50)
    
    
    
    
    # MOVE ON TO GETTING ARTIST NAME
    print("here")
    
    DISPLAY.fill(CONFIG.palette[4]) 
    
    artist_name = ""
    
    DISPLAY.text("Artist name", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Song title") // 2)), y = 20, color = CONFIG.palette[1])
    DISPLAY.text("Proceed: ENTER", x = 125, y =120, color = CONFIG.palette[1])

    DISPLAY.show()
    
    while True:
        keys = INPUT.get_new_keys()
        if keys:
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter in keys:
                    if len(artist_name) < 22:
                        artist_name += letter
                        break
            if 'BSPC' in keys:
                if len(artist_name) > 0:
                    artist_name = artist_name[:-1]
                    
            if 'ENT' in keys:
                if len(artist_name) > 0:
                    break
            
        DISPLAY.rect(10, 40, 220, 16, CONFIG.palette[7], fill = True)

        DISPLAY.text(artist_name, x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width(artist_name) // 2)), y = 44, color = CONFIG.palette[1])
        DISPLAY.show()
        time.sleep_ms(50)
    
    
    
    upload_flag = False
    save_to_sd_card_flag = False
    
    DISPLAY.fill(CONFIG.palette[4])
    
    DISPLAY.text("Upload? (Y/N)", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Upload? (Y/N)") // 2)), y = 20, color = CONFIG.palette[1])
    
    DISPLAY.show()
    
    while True:
        keys = INPUT.get_new_keys()
        if keys:
            if "y" in keys:
                upload_flag = True
                break
            else:
                break
    
    
    DISPLAY.fill(CONFIG.palette[4])
    
    DISPLAY.text("Save To SD Card? (Y/N)", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Save To SD Card? (Y/N)") // 2)), y = 20, color = CONFIG.palette[1])
    
    DISPLAY.show()
    
    while True:
        keys = INPUT.get_new_keys()
        if keys:
            if "y" in keys:
                save_to_sd_card_flag = True
                break
            else:
                break
    
    
    startup_layout("saving/uploading song")
    
    length_secs = 0
              
    song_data = {
        "metadata": {
            "title": song_title,
            "artist":  artist_name,
            "length_secs": length_secs,
            "length_num_notes": len(recording_notes_played)
            
            
            },
            "notes": []
        
        }
    
    for i in range(len(recording_notes_played) - 1):
        current = recording_notes_played[i]
        next_note = recording_notes_played[i + 1]
        gap = next_note[1] - current[1]
        song_data["notes"].append({"tine": current[0], "gap_duration": gap})
    
    
    song_data["notes"][-1]["gap_duration"] = 0
    
    total_gap = sum(note["gap_duration"] for note in song_data["notes"])
    
    song_data["metadata"]["length_secs"] = total_gap // 1000
        
    if upload_flag:
        sock = connect_to_kalimba(address)
        
        packet = "save_song"
        
        sock.sendto(packet, address)
        
        sock.settimeout(5)
        
        try:
            data = sock.recv(1024)
        except OSError:
            startup_layout("FAILED TO SEND SOCK EXITING")
            time.sleep(2)
            sys.exit()
        
        
        if data.strip() != b"send":
            startup_layout("FAILED TO SEND SOCK EXITING")
            time.sleep(2)
            sys.exit()
        else:
            song_data = json.dumps(song_data).encode()
            sock.sendto(song_data, address)
            startup_layout("SENT ALL SONG DATA")
    
    if save_to_sd_card_flag:
        pass
        
    time.sleep(1)
    clear_frame()



def connect_to_kalimba(address):
    
    
    attempts_count = 0
    startup_layout("Connecting")
    # Create a station interface (STA mode)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("WIFI SSID", "WIFI PASSWORD")

    while not sta_if.isconnected():
        pass

    print("Connected! IP:", sta_if.ifconfig()[0])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    packet = "Disconnect"
    sock.settimeout(2)
    
    sock.sendto(packet.encode(), address)
    
    
    packet = "Connect"
    

    response = None
    while response is None:
        print("Sending connecting packet")
        sock.sendto(packet.encode(), address)
        time.sleep_ms(1000)
        try:
            response, addr = sock.recvfrom(64)

        except OSError:
            attempts_count += 1
            startup_layout("No response after " + str(attempts_count) + " tries")
            print("No response yet, retrying...")

    # Now wait for 'Finished'
    while response.strip() != b'Finished':
        startup_layout(response.decode('utf-8'))
        print(response.decode('utf-8'))
        time.sleep_ms(500)
        response, addr = sock.recvfrom(64)

    startup_layout("Ready!")
    print("READY!")
        
    time.sleep_ms(500)
        
    return sock



def main_menu_layout(connected_flag):
    clear_frame()
    

    
    address = ('192.168.50.124', 44444)
    
    
    DISPLAY.fill(CONFIG.palette[3])
    DISPLAY.rect(0, 0, 240, 20, CONFIG.palette[9], fill = True)
    DISPLAY.rect(0, 0, 20, 140, CONFIG.palette[9], fill = True)
    DISPLAY.rect(0, 115, 240, 20, CONFIG.palette[9], fill = True)
    DISPLAY.rect(220, 0, 20, 120, CONFIG.palette[9], fill = True)
    
    if connected_flag:
        DISPLAY.text("Connected", 150, 6, color = CONFIG.palette[1])
        DISPLAY.ellipse(230, 9, 4, 4, CONFIG.palette[8], fill = True)
    else:
        DISPLAY.text("Connected", 150, 6, color = CONFIG.palette[1])
        DISPLAY.ellipse(230, 9, 4, 4, CONFIG.palette[4], fill = True)
    
    DISPLAY.text("1: Connect", 30, 30, color = CONFIG.palette[1])
    DISPLAY.text("2: Disconnect", 30, 40, color = CONFIG.palette[1])
    DISPLAY.text("3: Select Song", 30, 50, color = CONFIG.palette[1])
    DISPLAY.text("4: Demo Mode", 30, 60, color = CONFIG.palette[1])
    DISPLAY.text("5: Clear Song", 30, 70, color = CONFIG.palette[1])
    

    DISPLAY.show()


def select_song_helper(list_of_songs):
    DISPLAY.rect(20, 20, 200, 115, CONFIG.palette[9], fill = True)
    count = 1
    for i in list_of_songs:
        DISPLAY.text((str(count) + ". " +  str(i[:-5])), x = 24, y = 21 + (count * 8), color = CONFIG.palette[1])
        count += 1


def select_song(sock, address):
    clear_frame()
    DISPLAY.fill(CONFIG.palette[3])
    
    DISPLAY.show()
    
    sock.sendto("get_songs", address)
    
    sock.settimeout(5)  # or however many seconds you want

    try:
        list_of_songs, addr = sock.recvfrom(1024)
    except OSError:
        print("Timed out waiting for song list")
        list_of_songs = None
        addr = None
        startup_layout("Failed!! song list not recieved")
        return
    
    if list_of_songs:
        songs = json.loads(list_of_songs.decode())
    else:
        startup_layout("Failed to decode songs")
        return
    
    
    current_page = 1
    num_per_page = 12
    num_of_pages = math.ceil(len(songs) / num_per_page) + 1
    index = 0
    selected_song = 0
    update_graphics = True
    while True:
        
        if update_graphics:
            # select song header
            DISPLAY.rect(0, 0, 240, 15, CONFIG.palette[3], fill = True)
            DISPLAY.text("Select Song", x = ((_MH_DISPLAY_WIDTH // 2) - (DISPLAY.get_total_width("Select Song") // 2)), y = 5, color = CONFIG.palette[5])
            
            DISPLAY.rect(20, 20, 200, 115, CONFIG.palette[9], fill = True)
            DISPLAY.text((str(current_page) + "/" + str(num_of_pages - 1)), x = 200, y = 7, color = CONFIG.palette[5])

            index = (current_page - 1) * num_per_page
            select_song_helper(songs[index : index + num_per_page])
            
            update_graphics = False
            DISPLAY.show()
            print(index)
            print(current_page)
            
        keys = INPUT.get_new_keys()
        if keys:
            if "1" in keys:
                selected_song = index + 0
                break
        
            elif "2" in keys:
                selected_song = index + 1
                break
            
            elif "3" in keys:
                selected_song = index + 2
                break
            
            elif "4" in keys:
                selected_song = index + 3
                break
            
            elif "5" in keys:
                selected_song = index + 4
                break
            
            elif "6" in keys:
                selected_song = index + 5
                break
            
            elif "7" in keys:
                selected_song = index + 6
                break
            
            elif "8" in keys:
                selected_song = index + 7
                break
            
            elif "/" in keys:
                if current_page < (num_of_pages - 1):
                    current_page += 1
                    update_graphics = True
                    
            elif "," in keys:
                if current_page > 1 :
                    current_page -= 1
                    update_graphics = True
            
        
        time.sleep_ms(50)

    print("selected song: " + songs[selected_song])
    
    sock.sendto("play_song", address)
    sock.sendto(str(songs[selected_song]), address)
    
    sock = None


def main_menu():
    demo_mode = False
    
    reload_main_menu_flag = False
    connected_to_kalimba_flag = False
    
    
    clear_frame()
    
    address = ('192.168.50.124', 44444)
    
    
    sock = None
    
    main_menu_layout(reload_main_menu_flag)
    
    while True:
        keys = INPUT.get_new_keys()
        if keys:
            
            print(keys)
            
            if "1" in keys:
                if sock == None:
                    demo_mode = False
                    sock = connect_to_kalimba(address)
                    player(sock,address, demo_mode)
                    reload_main_menu_flag = True
                    connected_to_kalimba_flag = True
                else:
                    player(sock,address, demo_mode)
                    reload_main_menu_flag = True
            
            elif "2" in keys:
                if sock != None:
                    sock.sendto("Disconnect", address)
                    reload_main_menu_flag = True
                    connected_to_kalimba_flag = False
                    startup_layout("Disconnected")
                    time.sleep(2)
                    sock = None
                
                else:
                    sock = connect_to_kalimba(address)
                    sock.sendto("Disconnect", address)
                    startup_layout("Disconnected")
                    time.sleep(2)
                    reload_main_menu_flag = True
                    connected_to_kalimba_flag = False
                    sock = None
            
            elif "3" in keys:
                if sock != None:
                    connected_to_kalimba_flag = True
                    reload_main_menu_flag = True
                    select_song(sock, address)
                else:
                    sock = connect_to_kalimba(address)
                    connected_to_kalimba_flag = True
                    reload_main_menu_flag = True
                    select_song(sock, address)
                    
            elif "4" in keys:
                demo_mode = True
                reload_main_menu_flag = True
                connected_to_kalimba = False
                player(sock, address, demo_mode)
                
                
            elif "5" in keys:
                sock = connect_to_kalimba(address)
                sock.sendto("Clear_song", address)
                startup_layout("Cleared song")
                sock.sendto("Disconnect", address)
                time.sleep(1)
                reload_main_menu_flag = True
                    
        if reload_main_menu_flag:
            main_menu_layout(connected_to_kalimba_flag)
            reload_main_menu_flag = False
            
        time.sleep_ms(50)
    





def main_loop():
    main_menu()


main_loop()






