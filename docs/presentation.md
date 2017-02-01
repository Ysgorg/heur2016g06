todo cont


# Presentation

This doc summarises the project. 

## What we did

### Test kit

## Problem Analysis

2d grid, continous coordinates. 
place X objects according to restrictions.

### Constraints

|constraint|assignment|advanced assignment|heuristic value|
|m:b:h num residences proportion|2:3:5|\*|more valuable buildings->more value|
|m:b:h values|\*||
|m:b:h bonus over |\*||
|width|200|200|more area -> more residences -> more value|
|height|170|170|more area -> more residences -> more value|
|enable playground|True|False|costly playgrounds and restri|
|maximum playground distance|50|*null*|higher distance->fewer required playgrounds->more value|
|max number of waterbodies|4|4|higher max -> smaller waterbodies -> more placement freedom|
|water body sides ratio|4:1|4:1||

### Heuristics

 - M >= B >= F: it's more important to increase the clearance of a mansion than a bungalow, and a bungalow than a familyhome
 - put water in unusable area: either where playgrounds don't reach or next to residences with large minimal distances
 

### Reduction to tiling problem

 - We can translate the 
 - A residence type's minimum clearance

### Desired algorithm attributes

 - is generic: works well with any constraint set
 - produces a high-value plan fast

 