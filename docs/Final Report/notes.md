---
output:
  pdf_document: default
---

# Presentation

This doc summarises the project.

## Abstract

????????????

## Research Goal/Question

TODO: Probably change again

**Research Goal**
To find the highest plan value in a certain number of iterations, by varying parameters of various algorithms, optimised by simulated annealing.

**Research Question**
What combination of algorithm and parameters produces the highest plan value in a fixed number of iterations?

## What we did

 - Analyzed the problem
 - Proposed heuristics
 - Implemented an algo making heavy use of knowledge
 - Implemented searching methods for good parameters
 - Got and compared results
 - Suggested best approach
 
## Different approaches

### First approach
 
 - used only some heuristic knowledge
 - searched for good parameters for naive tile placement algorithms
 - takes much time
 - yields kind of OK scores
 - generifies for different problem instances
 
Problems: took a lot of development time that would have been better invested in the second approach

### Second approach

 - heavy use of heuristic knowledge 
 - takes little time
 - should yield higher scores than first approach
 - should ideally generify to different problem instances
 
problem: difficult to both encode heuristic knowledge AND make generic for different problem instances

## Problem Analysis

### Problem definition

#### Informal / human readable

???????????????????????+

### Formal / Pseudo-BNF

    area_rules := width, height
    water_rules := max_waterbody_sides_len_ratio , max_num_waterbodies, minimum_water_proportion
    playground_rules := width, height, enable_playground, max_playground_distance, playground_cost
    residence_class := width, height, value, percent_increase_per_extra meter of clearance
    familyhome_rules := residence_class
    bungalow_rules := residence_class
    mansion_rules := residence_class
    residence_rules := number_of_residences, mansion_rules, bungalow_rules, familyhome_rules
    problem := area_rules, water_rules, playground_rules, residence_rules
    solution := residences, waterbodies, playgrounds
    score(problem, solution) := # sum of values of solution.residences minus cost of solution.playgrounds
    isvalid(problem, solution) := # True iff problem constraints are met
    optimal_solution := # is valid and has score higher than or equal to any other possible solution to the same problem

The ideal algorithm would find an optimal solution for any problem.

### Constraints and heuristic impacts / adaptions / notes

|constraint|assignment|advanced assignment|heuristic value|
|---------|---------|------------|----------|
|m:b:h num residences proportion|2:3:5|\*|more valuable buildings->more value|
|m:b:h values|\*||
|m:b:h bonus over |\*||
|width|200|200|more area -> more residences -> more value|
|height|170|170|more area -> more residences -> more value|
|enable playground|True|False|costly playgrounds and less placement freedom|
|maximum playground distance|50|*null*|higher distance->fewer required playgrounds->more value|
|max number of waterbodies|4|4|higher max -> smaller waterbodies -> more placement freedom|
|water body sides ratio|4:1|4:1|larger maximum ratio -> more placement freedom|

### Heuristics

*numbers are for reference, not some ordering*

 1. more clearance is better
 2. prefer increasing clearances of more valueable residence
 3. clearance should not go unshared
 4. a new residence should not be placed in a way that reduces an already placed
 5. put water in unusable area
 6. put playgrounds in a way that maximize area and minimizes number of playgrounds

![partial implementation](images/corner-rows.png)

## First, more brute approach

did lots of computation without enough usage of knowledge

... elaborate how much?

![results, without legend](images/without-legend.png)

![results, with legend](images/with-legend.png)

