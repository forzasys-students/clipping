import json
import re
from datetime import datetime, timedelta
import Clipping



file_path= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\meta_1089.txt'
file_path2= r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\videoer\1089\game_1089.mp4'
#   match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$',line)
      #if match == line:
      #   continue

def count_lines(filename):
    with open(filename) as f:
        return sum(1 for i in f)
    


with open(file_path, 'r') as infile, open('output.json', 'w') as outfile:
    tall = count_lines(file_path)
    outfile.write("{")
    match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$', infile.readline())
    startvideo = 0

    if match:
        timestamp = match.group(1)
        date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        startvideo = date_time.strftime('%H:%M:%S')

    for i, line in enumerate(infile):
        line = line.replace("'", '"') 
        line = line.replace(',"', ":")
        line = line[:-2]  #fjerner \n og " som er på slutten av linja
        outfile.write(line)
        if i != tall - 2: 
            outfile.write(",\n")

    outfile.write("}")


with open("config.json", 'r') as f:
    config = json.load(f)

    action = config.get("action")
    start = config.get("start")
    end = config.get("end")


with open("output.json") as f:
    data = json.load(f)
for key in data:
    if data[key]["action"] == action:
        print(data[key]["action"])
        tid = datetime.strptime(key, "%Y-%m-%d %H:%M:%S.%f")
        nystart = tid - timedelta(seconds=start)
        start2 = datetime.strptime(nystart.strftime('%H:%M:%S'), '%H:%M:%S').time()
        nyslutt = tid + timedelta(seconds=end)
        slutt2 = datetime.strptime(nyslutt.strftime('%H:%M:%S'), '%H:%M:%S').time()
        print(slutt2)
        #print(startvideo)
        #print(start2)
        #print(slutt2, "\n")

        diff1 = datetime.combine(datetime.min, start2) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())
        print(diff1)
        diff2 = datetime.combine(datetime.min, slutt2) - datetime.combine(datetime.min, datetime.strptime(startvideo, '%H:%M:%S').time())
        print(diff2, "\n")

        #print ("\n")
        Clipping.trim(file_path2,"test.mp4", diff1, diff2)
        
      







#formatted_data = json.dumps(data, indent=4)
#print(formatted_data)
"""
with open(file_path, 'r') as infile, open('output.json', 'w') as outfile:
   outfile.write("{")
   match = re.search(r'^#\s*Video start timestamp:\s*(.*?)\s*$', infile.readline()) # skipper første linje
   for line in infile:
      line = line.replace("'", '"')
      line = line.replace(',"', ":")
      line = line[:-2] # fjerner siste \n og "
      outfile.write(line)
      outfile.write(",\n")
   outfile.write("}")
 """
"""with open(file_path, 'r') as infile, open('output.json', 'w') as outfile:
    lines = infile.readlines()
    outfile.write("{")
    for line in lines[1:-1]:  # iterate over all but the first and last lines
        line = line.replace("'", '"')
        line = line.replace(',"', ":")
        line = line[:-2] # remove last two characters (',\n')
        outfile.write(line)
        outfile.write(",\n")
    outfile.write("}")
 """
        # Remove quotes at the beginning and end of the line
#        line = line.strip().strip("'")
#        try:
#            # Parse the JSON string in the line
#            json_dict = json.loads(line)
#            # Extract the value of the "action" key
#            action = json_dict["action"]
#            print(action)
#        except json.decoder.JSONDecodeError as e:
#            print(f"Error parsing JSON object in line: {line}")
#            print(e)
#            counter+=1

#print(counter)









 
 
       # date_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        #startvideo = date_time.strftime('%Y-%m-%d %H:%M:%S')

 




#print(__file__)
#script_dir = os.path.dirname(__file__)
#file = "data\data.txt"
#abs_file_path = os.path.join(script_dir, file)

#with open(abs_file_path) as f:
 #   data = json.load(f)


#print(data[1])


#jtopy = json.dumps(data)
#json_dict = json.loads(jtopy)

#('C:\\Users\\aulic\Downloads\Download-video_test\Download-video_test\\videoer\data\data.txt')

#string = '2020-06-21 16:02:12.000000','{"team": {"id": 6, "type": "team", "value": "Aalesund"},"action": "free kick", "offending player": {"id": 683, "type": "player", "value": "Flamur Kastrati"}}'
#json_string = string.split(",")[1]  # Extract the second part of the string after the comma
#data = json.loads(json_string)  # Convert the JSON string to a dictionary