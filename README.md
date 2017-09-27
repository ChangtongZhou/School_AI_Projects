# School_AI_Projects
This demonstrates my school projects in Artificial Intelligence  

Purpose: To gain experience with problem solving agents and the A⋆ algorithm

Related Course Outcomes:

The main course outcomes covered by this assignment are:

LO1 -- By code or by hand find solution nodes in a state space using the A⋆ algorithm.

Specification:

Nario is an upwardly mobile video game character. When presented a n x m, text-based maze, Nario always strives to climb to the top floor using the A*-algorithm. Below is an example of the kind of maze Nario might appear in:

#.........          
=.======.=
..=.......      
====.=====
........=.
=.=====.==
=.........
==.=======
.....@....

The meaning of this Nario maze is as follows:

In the above Nario, is represented by the @.
The goal will always be in the top left and is represented by #.
An obstacle is represented by =
All other squares in the n x m board have a '.'
The '#' is the goal position.
In one turn, Nario can move one square to the left, right or up of his current location provided there are no obstacles in the square he is going to move to.
Nario can move off the edge of the board to the left or right and will wrap-around to the other side of the board, again, provided there is no obstacle blocking this move.
Input boards will always place Nario somewhere on the bottom row of the board.
For this homework you will write a Python program to get Nario to the top of the maze. Here are some guidelines for your program:

Your program will be run from the command line with a line like:
python nario.py file_name heuristic
Here file_name is the name of some text file with a Nario board. heuristic can be one of the three values manhattan, euclidean, my_own.
Your program should use the A* algorithm to determine a sequence of moves to take Nario from the bottom row of the board to the #. If the input board was:
#..
==.
@.. 
your output should look like:


#..
==.  Nario wraps around by going left off board
..@

#..
==@
...

#.@
==.
...

@..
==. Nario wraps around by going right off board
...
