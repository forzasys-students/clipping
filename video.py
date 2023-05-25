import json
import re
from datetime import datetime, timedelta
import sys
import ffmpeg
import Clipping
import os 

# Path to the JSON file containing metadata
JSON_PATH = r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\meta_1089.txt'
# Path to the game file
VIDEO_PATH = r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\game_1089.mp4'


# Function to extract the start time of the video from the metadata file
def startvideo2(infile):
    match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$', infile.readline())

    if match:
        timestamp = match.group(1)
        date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        startvideo = date_time.strftime('%H:%M:%S')
        return startvideo


# Function to count the number of lines in a file
def count_lines(filename):
    with open(filename) as f:
        return sum(1 for i in f)


# Function to format the JSON data and write it to a new file
def formatjson():
    with open(JSON_PATH, 'r') as infile, open('output.json', 'w') as outfile:
        countLines = count_lines(JSON_PATH)
        amount_lines = countLines - 2
        startvideo = startvideo2(infile)
        outfile.write("{")

        for i, line in enumerate(infile):
            line = line.replace("'", '"')
            line = line.replace(',"', ":")
            line = line.replace('"\n', "")
            outfile.write(line)
            if i != amount_lines:
                outfile.write(",\n")

        outfile.write("}")

        return startvideo
    

def clipname(start_clip, config_action, folder_name="videos"):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    except OSError as e:
            print(f"Error creating folder: {e}")

    matchtime_str = str(start_clip)
    formatString = matchtime_str.replace(':', "-")

    output_filename = f"{folder_name}/{config_action}_{formatString}.mp4"

    return output_filename


# Function to perform video clipping based on specified timings
def clipTimings(config_action, key, config_start, config_stop):
    timestamp = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
    normaltime_start = timestamp - timedelta(seconds=config_start)
    start = datetime.strptime(normaltime_start.strftime('%H:%M:%S'), '%H:%M:%S').time()
    normaltime_end = timestamp + timedelta(seconds=config_stop)
    end = datetime.strptime(normaltime_end.strftime('%H:%M:%S'), '%H:%M:%S').time()

    start_clip = datetime.combine(datetime.min, start) - datetime.combine(
        datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())
    end_clip = datetime.combine(datetime.min, end) - datetime.combine(
        datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())

    output_filename = clipname(start_clip, config_action)

    Clipping.trim(VIDEO_PATH, output_filename, start_clip, end_clip)


def framerate(config_start, config_stop):
    probe = ffmpeg.probe(VIDEO_PATH)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if video_stream is None:
        print('No video stream found')
        exit(1)

    frame_rate_str = video_stream['avg_frame_rate']
    x, y = frame_rate_str.split('/')
    frame_rate = int(x) / int(y)
    frames_bef = config_start / frame_rate
    frames_aft = config_stop / frame_rate

    return frames_bef, frames_aft


def duration(config_start, config_stop):
    duration = config_start / 2
    duration2 = config_start / 4
    duration3 = duration + duration2

    start_time = [0, duration2, duration, duration3, config_start][config_stop - 1]
    end_time = [config_start, duration3, duration, duration2, 0][config_stop - 1]

    return start_time, end_time


# Function to process different types of video events
def videoTypes(config_action, cutType, numEvents, config_start, config_stop):
    i = 0
    action_found = False 
    for key in data:
        if data[key]["action"] == config_action:
            action_found = True
            if cutType == 1:  # cuttype seconds
                i += 1
                clipTimings(config_action, key, config_start, config_stop)

            elif cutType == 2:  # cuttype frames
                i += 1
                frames_bef, frames_aft = framerate(config_start, config_stop)
                clipTimings(config_action, key, frames_bef, frames_aft)

            elif cutType == 3:  # cuttype duration
                i += 1
                start_time, end_time = duration(config_start, config_stop)
                clipTimings(config_action, key, start_time, end_time)
        
        if i == numEvents:
            break
        
    if not action_found:
        print('ERROR: {} Did not find any action for your configuration in the JSON file'.format(sys.argv[0]))


if __name__ == '__main__':
    # Validate command-line arguments
    if (len(sys.argv) not in [6] or
            sys.argv[1] not in ['goal', 'red_card', 'yellow_card', 'free_kick', 'shot', 'offside', 'substitution', 'corner','penalty', 'tja'] or
            sys.argv[2] not in ['1', '2', '3'] or
            not sys.argv[3].isdigit() or
            not sys.argv[4].isdigit() or
            not sys.argv[5].isdigit() or
            sys.argv[2] == '3' and sys.argv[5] not in ['1', '2', '3', '4', '5']):
        if sys.argv[2] == '3':
            print('Usage: {} [goal|red_card|yellow_card|free_kick|shot|substitution|corner|penalty]'
            ' [1|2|3] [number of events] [amount of duration] [1|2|3|4|5]'
            .format(sys.argv[0]))
        else :  
            print('Usage: {} [goal|red_card|yellow_card|free_kick|shot|substitution|corner|penalty]'
            ' [1|2|3] [number of events] [amount of seconds before] [amount of seconds after]'
            .format(sys.argv[0]))
        exit(1)

    eventType = sys.argv[1].replace('_', ' ')
    cutType = int(sys.argv[2])
    numEvents = int(sys.argv[3])
    secondsBef = int(sys.argv[4])
    secondsAft = int(sys.argv[5])

    startvideo = formatjson()

    with open("output.json", 'r') as f:
        data = json.load(f)

    videoTypes(eventType, cutType, numEvents, secondsBef, secondsAft)
