# README

You can run the pipeline (function 1) in the following ways.

(A) Clip a configurable number of events of configurable event type with the clipping points specified as seconds before and seconds after:

```
python video.py -eventTypeX -<numEvents> -cutType1 -<secondsBef> -<secondsAft>
```

(B) Clip a configurable number of events of configurable event type with the clipping points specified as frames before and frames after:

```
python video.py -eventTypeX -<numEvents> -cutType2 -<frameBef> -<frameAft>
```

python video.py -eventTypeX -<numEvents> -cutType3 -<duration> 
python video.py -eventTypeX -<numEvents> -cutType4  …
