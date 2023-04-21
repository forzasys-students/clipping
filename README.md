# README

## Pipeline Function 1: Clipping Local Assets

You can run the pipeline function 1 in the following ways.

### (A) 

Clip a configurable number of events of configurable event type with the clipping points specified as seconds before and seconds after:

```
python video.py -eventTypeX -<numEvents> -cutType1 -<secondsBef> -<secondsAft>
```

### (B) 

Clip a configurable number of events of configurable event type with the clipping points specified as frames before and frames after:

```
python video.py -eventTypeX -<numEvents> -cutType2 -<frameBef> -<frameAft>
```

### (C) 

Clip a configurable number of events of configurable event type with the total clip duration specified:

```
python video.py -eventTypeX -<numEvents> -cutType3 -<duration> 
```

Alternatives: percentage of duration D, centered around event annotation E

Alternative | Before E | After E |
| ------------- | ------------- | ------------- |
| (C1) | 0% | 100% |
| (C2) | 25% | 75% |
| (C3) | 50% | 50% |
| (C4) | 75% | 25% |
| (C5) | 100% | 0% |


### (D) 

...

```
python video.py -eventTypeX -<numEvents> -cutType4  …
```



## Pipeline Function 2: Clipping Remote Assets using API


```
python myawesomescript.py -clipType <TYPE>
```

| Types | Before Event Annotation | After Event Annotation |
| ------------- | ------------- | ------------- |
| (1) | first scene transition (any) | first scene transition (any)|
| (2) | first scene transition (any) | first logo transition |
| (3) | first scene transition (any) | second logo transition |
| (4) | ... | ... |
| (5) | ... | ... |
  
  
  
  
  
