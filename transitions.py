import os
import json
import sys
import Clipping





def transition_times(cut1, cut2, number):

    with open(transitions_file, 'r') as f:
        transitions = json.load(f)

    first = True
    action_after = None
    action_before = None
    i= 0

    for transition in transitions:
        start = int(transition["start_frame"])

        if start >= frame:
            first = False


        if cut1 == None and cut2 == None:

            if first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]

            if not first:

                action_after = transition["start_frame"]
                break
        
        elif cut1 == None and isinstance(cut2, str):

            if first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]

            if not first:
                if cut2 == transition["subcategory"]:
                    action_after = transition["start_frame"]
                    i+=1

                    if i == number:
                        break

        elif isinstance(cut1, str) and cut2 == None:

            if first:
                if cut2 == transition["subcategory"]:
                    action_before = transition["end_frame"]
                    clip_name = transition["subcategory"]
                    i+=1

                    if i == number:
                        break

            if not first:
                action_after = transition["start_frame"]


        elif cut1 == "logo" and cut2 == "logo":

            if cut1 == transition["subcategory"] and i==0:
                clip_name = transition["subcategory"]
                action_before = transition["end_frame"]
                i+=1

            elif cut2 == transition["subcategory"] and i==1:
                action_after = transition["start_frame"]
                break

                

        else:

            if transition["subcategory"] == cut1 and first:
                action_before = transition["end_frame"]
                clip_name = transition["subcategory"]

            if transition["subcategory"] == cut2 and not first:
                action_after = transition["start_frame"]
                break



    if (action_before == None):
        print('Could not find the transition before the event'.format(sys.argv[0]))
        exit(1)

    elif( action_after == None):
        print('Could not find the transition after the event'.format(sys.argv[0]))
        exit(1)

    print(action_before, " ", action_after)

    int_actionbef = int(action_before)
    int_actionaft = int(action_after)
    secondsbef = int_actionbef/25
    secondsaft = int_actionaft/25


    output_filename = file_name(clip_name)

    Clipping.trim(video_path, output_filename, secondsbef, secondsaft)


def file_name(navn):
        
    eventType = navn.replace(' ', '_')
    folder_name = "videos"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    output_filename = f"{folder_name}/{eventType}_{sys.argv[1]}.mp4"
    return output_filename



if __name__ == '__main__':
  

    if len(sys.argv) not in [2] or\
        sys.argv[1] not in ['1','2','3','4','5']:
        print('Usage: {} [1, 2, 3, 4, 5]'.format(sys.argv[0]))
        exit(1)

    transitions_file = r'C:\Users\aulic\Downloads\Download-video_test 2\Download-video_test\transition_3714.json'
    video_path = r'C:\Users\aulic\Downloads\Download-video_test 2\yel_card.mp4'
    event = 26
    frame = 25 * event


    cut1 = None
    cut2 = None
    counter = 1

    if (sys.argv[1] == '2'):
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
