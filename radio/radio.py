import time
import math
import serial
from glob import glob
import pygame

# ------ SETTINGS ----------
noise_easing_factor = 1  # from 0 to 1 (0 for no easing, 1 for full easing)
track_easing_factor = 1
noise_ratio = 1.5  # must be higher than 0 (if above 1, then noise will be present for larger ranges than not)
track_ratio = 1  # must be higher than 0 (if above 1, then tracks will be absent for larger ranges than not)
# ------ SETTINGS END ------

freq = 44100     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 2     # 1 is mono, 2 is stereo
buffer = 2048    # number of samples (experiment to get right sound)

def map_range(x, in_min, in_max, out_min, out_max) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(x, min, max) -> float:
    if x < min: return min
    if x > max: return max
    return x

def ease(x, factor) -> float:
    if factor == 0: return x
    return (2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2) * factor + x * (1 - factor)

def extend(x, low, high):
  if x < 0: return x * low
  return x * high

def main() -> None:
    # get audio files
    noise_paths = glob('noise/*.ogg')
    if not len(noise_paths):
        raise RuntimeError('no .ogg file in noise folder.')

    track_paths = glob('tracks/*.ogg')
    if not len(track_paths):
        raise RuntimeError('no .ogg file in tracks folder.')

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
    pygame.mixer.music.load(track_paths[1])
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(loops=-1, start=5)

    # main loop
    time_start = time.time()
    current_track_index = 0
    prev_track_index = 0
    current_pos = 0
    current = 0
    try:
        while True:
            # get current potentiometer position
            line = ser.readline()
            if line:
                try:
                    current = clamp(int(line.strip()), 0, 1023)
                except Exception:
                    current = 0

                current_pos = map_range(current, 0, 1023, 0, 2 * math.pi * len(tracks))

            # set volumes
            noise_volume = ease(map_range(extend(math.cos(current_pos), noise_ratio, 1/noise_ratio), -noise_ratio, 1/noise_ratio, 0, 1), noise_easing_factor)
            channel_1.set_volume(noise_volume)
            track_volume = ease(map_range(extend(math.cos(current_pos), track_ratio, 1/track_ratio), -track_ratio, 1/track_ratio, 1, 0), track_easing_factor)
            pygame.mixer.music.set_volume(track_volume)

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

            # wait for 0.1 sec
            pygame.time.wait(100)

            ser.reset_input_buffer()

    except Exception:
        print('unexpected error.')
    

if __name__ == '__main__':
    main()