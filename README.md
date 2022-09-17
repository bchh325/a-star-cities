# a-star-cities
Implementation of A* Algorithm to determine which is the shortest path in terms of distance to get from one city to another.

Uses straight line distance from cities as a heuristic to determine the next best fit city to expand.

Running the algorithm:
>py a-star.py (city1) (city2) #city names are case sensitive and can be found in coordinates.txt

ex. 

>py a-star.py LongBeach SanFrancisco

From city: LongBeach  
To city: SanFrancisco  
Best Route: LongBeach - LosAngeles - Fresno - SanJose - SanFrancisco  
Total distance: 442.50 mi  
