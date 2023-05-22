import os
import json
import sys
import Clipping


TRANSITIONS_FILE = r'C:\Users\aulic\Downloads\Download-video_test 2\json_files\transition_sub.json'
VIDEO_PATH = r'C:\Users\aulic\Downloads\Download-video_test 2\substitution.mp4'


def errorhandling(action_before, action_after):
    if (action_before == -1):
        print('Could not find the transition before the event'.format(sys.argv[0]))
        exit(1)

    elif (action_after == None):
        print('Could not find the transition after the event'.format(sys.argv[0]))
        exit(1)


def transition_times(cut1, cut2, number):

    with open(TRANSITIONS_FILE, 'r') as f:
        transitions = json.load(f)

    first = True
    action_before = -1
    action_after = None
    count= 0
    last_transition = None
    scene_transition = None 
    in_transitions = {"Long Shot",  "Close-up Shot"}
    out_transitions = {"Medium Shot", "Full Shot"}

    for transition in transitions:
        start = int(transition["start_frame"])

        if start >= frame:
            first = False

        # cut to the first zoom in before event and first zoom out after
        if sys.argv[1] == '6': 
            last_transition = scene_transition
            scene_transition = transition["subcategory"]   
            if first:
                if scene_transition in out_transitions and last_transition in in_transitions:
                    clip_name = transition["subcategory"]
                    action_before = transition["end_frame"]
            else:
                if last_transition in in_transitions and scene_transition in out_transitions:
                    action_after = transition["start_frame"]
                    break

        # cut the first transition before and after the event 
        elif cut1 is None and cut2 is None:
            if first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]
            else:
                action_after = transition["start_frame"]
                break

        # cut the first scene transition and a certain transition of a certain amount of instances after the event
        elif cut1 is None and isinstance(cut2, str): 
            if first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]
            else:
                if cut2 == transition["subcategory"]:
                    action_after = transition["start_frame"]
                    count += 1
                    if count == number:
                        break

        # cut the first instance of the certain transition before and the first transition after the event
        elif isinstance(cut1, str) and cut2 is None: 
            if first:
                if cut1 == transition["subcategory"]:
                    action_before = transition["end_frame"]
                    clip_name = transition["subcategory"]
            else:
                action_after = transition["start_frame"]

        # cut the first and second logo transition after the event
        elif cut1 == "logo" and cut2 == "logo":
            if not first:
                if cut1 == transition["subcategory"] and count == 0:
                    clip_name = transition["subcategory"]
                    action_before = transition["end_frame"]
                    count += 1
                elif cut2 == transition["subcategory"] and count == 1:
                    action_after = transition["start_frame"]
                    break

        # cut the first event with the correct transition before and after
        else: 
            if transition["subcategory"] == cut1 and first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]
            elif transition["subcategory"] == cut2 and not first:
                action_after = transition["start_frame"]
                break


    errorhandling(action_before, action_after)

    secondsbef = int(action_before) / 25
    secondsaft = int(action_after) / 25

    output_filename = file_name(clip_name)

    Clipping.trim(VIDEO_PATH, output_filename, secondsbef, secondsaft)




def file_name(navn):
        
    eventType = navn.replace(' ', '_')
    folder_name = "videos"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    output_filename = f"{folder_name}/{eventType}_{sys.argv[1]}.mp4"
    return output_filename



if __name__ == '__main__':
    if len(sys.argv) not in [2] or\
        sys.argv[1] not in ['1','2','3','4','5','6']:
        print('Usage: {} [1, 2, 3, 4, 5, 6]'.format(sys.argv[0]))
        exit(1)
    
    event = 25
    frame = 25 * event
    cut1 = None
    cut2 = None
    counter = 1

    if (sys.argv[1] == '2'):
        cut1 = "Full Shot"
        cut2 = "logo"

    elif (sys.argv[1] == '3'):
        cut2 = "logo"
        counter = 2

    elif (sys.argv[1] == '4'):
        cut1 = "Full Shot"
        cut2 = "Close-up Shot"

    elif (sys.argv[1] == '5'):
        cut1 = "logo"
        cut2 = "logo"

    transition_times(cut1, cut2, counter)
