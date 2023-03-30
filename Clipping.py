import os
import ffmpeg
import json


def trim(in_file, out_file, nystart, nyslutt):
    print(nyslutt)
    print(nystart)


    if os.path.exists(out_file):
        os.remove(out_file)

    probe_result = ffmpeg.probe(in_file)
    in_file_duration = probe_result.get("format", {}).get("duration", None)
    print(f"In file duration: {in_file_duration}")


    input_stream = ffmpeg.input(in_file)
    pts = "PTS-STARTPTS"

    video = input_stream.trim(start=nystart, end=nyslutt).setpts(pts)
    audio = (input_stream.filter("atrim", start=nystart, end=nyslutt).filter_("asetpts", pts))

    video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)
    output = ffmpeg.output(video_and_audio, out_file, format="mp4")
    output.run()

# Example usage: trim video using timestamps from "config.json" file
