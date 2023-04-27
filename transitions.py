import os
import json
import ffmpeg
import sys
import Clipping

OVERWRITE_EXISTING_VIDEOS = False
quality_level = 500000
transitions_file = r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\transition.json'

video2 = r'C:\Users\aulic\Downloads\Download-video_test 2\output.mp4'


from_timestamp = 6800000
to_timestamp = 6939999
goal = 56
frames = 25*goal
print(frames, "mål frames")

def transition_times(hendelse1, hendelse2, type2):

    with open(transitions_file, 'r') as f:
        transitions = json.load(f)
    first = True
    actionaft2 = None
    actionbef2 = None

    for transition in transitions:
        start = int(transition["start_frame"])

        if start >= frames:
            first = False

        if type2 == True:
            if first:
                actionbef2 = transition["end_frame"]
            if not first:
                actionaft2 = transition["start_frame"]
                break

        else:
            if transition["subcategory"] == hendelse1 and first:
                actionbef2 = transition["end_frame"]
            if transition["subcategory"] == hendelse2 and not first:
                actionaft2 = transition["start_frame"]
                break

    if (actionaft2 == None and type2 == False):
        print('finner ikke hendelse før målet'.format(sys.argv[0]))
        exit(1)
    elif( actionbef2 == None and type2 == False):
        print('finner ikke hendelse etter målet'.format(sys.argv[0]))
        exit(1)
    print(actionbef2, " ", actionaft2)

    actionbef = int(actionbef2)
    actionaft = int(actionaft2)
    secondsbef = actionbef/25
    secondsaft = actionaft/25

    output_filename = f"{actionbef}_{hendelse1}.mp4"

    Clipping.trim(video2, output_filename, secondsbef, secondsaft)
    
    if __name__ == '__main__':
  

    if len(sys.argv) not in [2, 4] or \
    sys.argv[1] not in ['1','2'] or \
    (len(sys.argv) == 4 and \
    (sys.argv[2] not in ['Long_Shot', 'Medium_Shot', 'Close-up_Shot', 'Full_Shot'] or \
        sys.argv[3] not in ['Long_Shot', 'Medium_Shot', 'Close-up_Shot', 'Full_Shot'])) or \
    len(sys.argv) == 2 and sys.argv[1] == '1' or \
    len(sys.argv) == 4 and sys.argv[1] == '2':
        
        if (len(sys.argv) == 4):
            print('Usage: {} [1] [Long_Shot|Medium_Shot|Close-up_Shot|Full_Shot] [Long_Shot|Medium_Shot|Close-up_Shot|Full_Shot]'.format(sys.argv[0]))
        else:
            print('Usage: {} [2]'.format(sys.argv[0]))
        exit(1)

        

    if (sys.argv[1] == '1'):
        type1 = False

    else:
        type1 = True


    hendelse1 = None
    hendelse2 = None

    if sys.argv[1] == '1':
        hendelse1 = sys.argv[2].replace('_', ' ')
        hendelse2 = sys.argv[3].replace('_', ' ')


    transition_times(hendelse1, hendelse2, type1)
