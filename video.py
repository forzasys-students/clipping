import json
import re
from datetime import datetime, timedelta
import sys
import ffmpeg
import Clipping


file_path= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\meta_1089.txt'
file_path2= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\game_1089.mp4'




def startvideo2(infile):
    match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$', infile.readline())

    if match:
        timestamp = match.group(1)
        date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        startvideo = date_time.strftime('%H:%M:%S')
        return startvideo
    

def count_lines(filename):
    with open(filename) as f:
        return sum(1 for i in f)
    

def formatjson():
    with open(file_path, 'r') as infile, open('output.json', 'w') as outfile:
        countLines = count_lines(file_path)
        amount_lines = countLines-2
        outfile.write("{")
        startvideo = startvideo2(infile)

        for i, line in enumerate(infile):
            line = line.replace("'", '"') 
            line = line.replace(',"', ":")
            line = line.replace('"\n', "")
            outfile.write(line)
            if i != amount_lines: 
                outfile.write(",\n")

        outfile.write("}")

        return startvideo
    

def clipTimings(config_action, key, config_start, config_stop):
                
    timestamp = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
    normaltime_start = timestamp - timedelta(seconds=config_start)
    start = datetime.strptime(normaltime_start.strftime('%H:%M:%S'), '%H:%M:%S').time()
    normaltime_end = timestamp + timedelta(seconds=config_stop)
    end = datetime.strptime(normaltime_end.strftime('%H:%M:%S'), '%H:%M:%S').time()


    start_clip = datetime.combine(datetime.min, start) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())
    end_clip = datetime.combine(datetime.min, end) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())


    matchtime_str = str(start_clip)
    formatString = matchtime_str.replace(':', "-")

    output_filename = f"{config_action}_{formatString}.mp4"

    Clipping.trim(file_path2, output_filename, start_clip, end_clip)





def jsontimestamps(config_action, cutType, numEvents, config_start, config_stop):

    counter = 0
    if cutType == 1:

        for key in data:
            if data[key]["action"] == config_action:
                      
                clipTimings(config_action, key, config_start, config_stop)


                counter +=1
                if counter == numEvents:
                    break
                
               

    elif cutType == 2:
        for key in data:
            if data[key]["action"] == config_action:
                  
                probe = ffmpeg.probe(file_path2)

                video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

                if video_stream is None:
                    print('No video stream found')
                    exit(1)


                frame_rate_str = video_stream['avg_frame_rate']

                x, y = frame_rate_str.split('/')
                frame_rate = int(x) / int(y)


                frames_bef = config_start/frame_rate
                frames_aft = config_stop/frame_rate



                clipTimings(config_action, key, frames_bef, frames_aft)

                counter +=1
                if counter == numEvents:
                    break



    elif cutType == 3:
        for key in data:
            if data[key]["action"] == config_action:

                duration = config_start/2

                clipTimings(config_action, key, duration, duration)


                counter +=1
                if counter == numEvents:
                    break



 

#with open("config.json", 'r') as f:
 #   config = json.load(f)


if __name__ == '__main__':

    if (len(sys.argv) not in [5, 6] or
        sys.argv[1] not in ['goal', 'red_card', 'yellow_card', 'free_kick', 'shot'] or
        sys.argv[2] not in ['1', '2', '3'] or
        not sys.argv[3].isdigit() or
        not sys.argv[4].isdigit() or
        len(sys.argv) == 6 and not sys.argv[5].isdigit() or
        len(sys.argv) == 6 and sys.argv[2] == '3' or
        len(sys.argv) == 5 and not sys.argv[2] == '3'):
        
        if len(sys.argv) == 5:
            print('Usage: {} [goal|red_card|yellow_card|free_kick|shot] [1|2|3] [must number, antall] [must number, lengde klipp]'.format(sys.argv[0]))
    
        else:
            print('Usage: {} [goal|red_card|yellow_card|free_kick|shot] [1|2|3] [must number, antall] [must number, før] [must number, etter]'.format(sys.argv[0]))
        
        exit(1)






    eventType = sys.argv[1].replace('_', ' ')
    cutType = int(sys.argv[2])
    numEvents = int(sys.argv[3])
    secondsBef = int(sys.argv[4])

    if len(sys.argv) == 6:
        secondsAft = int(sys.argv[5])
    else:
        secondsAft = None


    startvideo = formatjson()

    with open("output.json", 'r') as f:
        data = json.load(f)

    jsontimestamps(eventType, cutType, numEvents, secondsBef, secondsAft)
