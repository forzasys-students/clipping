import json
import re
from datetime import datetime, timedelta
import Clipping



file_path= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\meta_1089.txt'
file_path2= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\game_1089.mp4'




def startvideo2(infile):
    match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$', infile.readline())
    print(match)

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
        tall = count_lines(file_path)
        antalllinjer = tall-2
        outfile.write("{")
        startvideo = startvideo2(infile)

        for i, line in enumerate(infile):
            line = line.replace("'", '"') 
            line = line.replace(',"', ":")
            line = line.replace('"\n', "")
            outfile.write(line)
            if i != antalllinjer: 
                outfile.write(",\n")

        outfile.write("}")

        return startvideo


def jsontimestamps():


    for i in config["action"]:
        config_action = (i["action"])
        config_start = (i["start"])
        config_stop = (i["end"])
        for key in data:
            if data[key]["action"] == config_action:

                tid = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
                nystart = tid - timedelta(seconds=config_start)
                start2 = datetime.strptime(nystart.strftime('%H:%M:%S'), '%H:%M:%S').time()
                nyslutt = tid + timedelta(seconds=config_stop)
                slutt2 = datetime.strptime(nyslutt.strftime('%H:%M:%S'), '%H:%M:%S').time()
            

                diff1 = datetime.combine(datetime.min, start2) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())
                diff2 = datetime.combine(datetime.min, slutt2) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())


                forskjell = str(diff1)
                jau = forskjell.replace(':', "-")

                output_filename = f"{config_action}_{jau}.mp4"
          
                Clipping.trim(file_path2, output_filename, diff1, diff2)

 

with open("config.json", 'r') as f:
    config = json.load(f)



startvideo = formatjson()


with open("output.json", 'r') as f:
    data = json.load(f) 

jsontimestamps()
