from typing import Union
import time
import math
import serial
from glob import glob
import pygame
import paho.mqtt.client as mqtt

# ------ SETTINGS ----------
noise_easing_factor = 1  # from 0 to 1 (0 for no easing, 1 for full easing)
track_easing_factor = 0.5
noise_ratio = 1.5  # must be higher than 0 (if above 1, then noise will be present for larger ranges than not)
track_ratio = 1  # must be higher than 0 (if above 1, then tracks will be absent for larger ranges than not)

mqtt_server = '192.168.88.22'
mqtt_port = 1883

initial_disable_max=50 #disable initial radio tuning for some amount. higher value means longer until noise is gone.

message_delay = 50  # time between readings and sending data
# ------ SETTINGS END ------

# pygame audio settings
freq = 44100     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 2     # 1 is mono, 2 is stereo
buffer = 2048    # number of samples (experiment to get right sound)

# global variables
noise_folder = 'noise/*.ogg'
tracks_folder = 'tracks/*.ogg'
volume = 0
last_send_pos = 0
reset = False
initial_disable = 0
last_initial_noise_factor = 0

def map_range(x: Union[float, int], in_min: Union[float, int], in_max: Union[float, int], out_min: Union[float, int], out_max: Union[float, int]) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(x: Union[float, int], min: Union[float, int], max: Union[float, int]) -> float:
    if x < min: return min
    if x > max: return max
    return x

def ease(x: Union[float, int], factor: float) -> float:
    if factor == 0: return x
    return (2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2) * factor + x * (1 - factor)

def extend(x: Union[float, int], low: float, high: float):
    if x < 0: return x * low
    return x * high

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("mqtt connected success")
    else:
        print(f"mqtt connected fail with code {rc}")

def on_message(client, userdata, msg) -> None:
    global noise_folder
    global tracks_folder
    global volume
    global reset
    global initial_disable

    if msg.topic == 'general':
        if msg.payload.decode('utf-8') == 'reset':
            noise_folder = 'noise/*.ogg'
            tracks_folder = 'tracks/*.ogg'
            volume = 0
            reset = True
            initial_disable=0
    elif msg.topic == 'radio/volume':
        try:
            volume = float(msg.payload)
        except Exception:
            volume = 0
    elif msg.topic =='radio/noise':
        noise_folder = f'{msg.payload.decode("utf-8")}/*.ogg'
        reset = True
        initial_disable=0
    elif msg.topic == 'radio/tracks':
        tracks_folder = f'{msg.payload.decode("utf-8")}/*.ogg'
        reset = True
        initial_disable=0

def main() -> None:
    # setup mqtt connection
    client = mqtt.Client() 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_server, mqtt_port, 60)

    # subscribe to relevant channels
    client.subscribe([('general', 0), ('radio/volume', 0), ('radio/noise', 0), ('radio/tracks', 0)])

    client.loop_start()

    client.publish('general', payload='radio ready', qos=0, retain=False)

    try:
        while True:
            play(noise_folder, tracks_folder, client)
    except KeyboardInterrupt:
        print('shutting down')
    finally:
        client.loop_stop()


def play(noise_glob: str, tracks_glob: str, mqtt_client: mqtt.Client) -> None:
    global reset
    global last_send_pos
    global last_initial_noise_factor

    # get audio files
    noise_paths = sorted(glob(noise_glob))
    if not len(noise_paths):
        raise RuntimeError('no .ogg file in noise folder.')

    track_paths = sorted(glob(tracks_glob))
    if not len(track_paths):
        raise RuntimeError('no .ogg file in tracks folder.')

    # todo sort

    noise_path = noise_paths[0]

    # setup serial
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=0.1)

    #set up the mixer
    pygame.mixer.init(freq, bitsize, channels, buffer)

    # setup channels
    channel_1 = pygame.mixer.Channel(1)

    # setup tracks
    noise = pygame.mixer.Sound(noise_path)
    tracks = [{'path': path, 'length': pygame.mixer.Sound(path).get_length(), 'position': 0} for path in track_paths]
    
    # play noise track
    noise.set_volume(1)
    channel_1.play(noise, loops=-1)
    pygame.mixer.music.load(track_paths[0])
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(loops=-1)

    # main loop
    time_start = time.time()
    current_track_index = 0
    prev_track_index = 0
    current_pos = 0
    current = 0

    while not reset:
        # get current potentiometer position
        line = ser.readline()
        if line:
            try:
                current = clamp(int(line.strip()), 0, 1023)
            except Exception:
                current = 0

            current_pos = map_range(current, 0, 1023, 0, 2 * math.pi * len(tracks))
            

            current_send_pos = int(map_range(current, 0, 1023, 0, 255))
            initial_disable+=abs(current_send_pos-last_send_pos)
            if current_send_pos != last_send_pos:
                mqtt_client.publish('radio/poti', payload=current_send_pos, qos=0, retain=False)
                last_send_pos = current_send_pos
                
            
            
        initial_noise_factor=clamp((1.0-initial_disable*1.0/initial_disable_max),0,1) #1=only noise, 0=radio working fully
        if initial_noise_factor != last_initial_noise_factor: #changed
            mqtt_client.publish('radio/initialnoise', payload=initial_noise_factor, qos=0, retain=False)
            last_initial_noise_factor=initial_noise_factor
            
        # set volumes
        noise_volume = ease(map_range(extend(math.cos(current_pos), noise_ratio, 1/noise_ratio), -noise_ratio, 1/noise_ratio, 0, 1), noise_easing_factor)
        noise_volume = clamp(initial_noise_factor+noise_volume,0,1) #increase noise during initial noise phase
        channel_1.set_volume(noise_volume * clamp(volume, 0, 1))
        track_volume = ease(map_range(extend(math.cos(current_pos), track_ratio, 1/track_ratio), -track_ratio, 1/track_ratio, 1, 0), track_easing_factor)
        track_volume = clamp(track_volume-initial_noise_factor,0,1) #reduce track volume during initial noise phase
        pygame.mixer.music.set_volume(track_volume * clamp(volume, 0, 1))

        # get which track to play
        # and play that track from its current position
        current_track_index = int(map_range(current, 0, 1024, 0, len(tracks)))
        if (current_track_index != prev_track_index):
            pygame.mixer.music.load(tracks[current_track_index]['path'])
            pygame.mixer.music.play(loops=-1, start=tracks[current_track_index]['position'])
            prev_track_index = current_track_index

        # get each track position
        for track in tracks:
            track['position'] = (time.time() - time_start) % track['length']

        print(current, current_pos, current_track_index)

        # wait
        pygame.time.wait(message_delay)

        # reset the serial buffer
        ser.reset_input_buffer()

        # do mqtt stuff
        # mqtt_client.loop()

    reset = False
    

if __name__ == '__main__':
    main()