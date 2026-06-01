#const horizon=4.

robot(1).
robot(2).

node(1,1).            node(3,1).
node(1,2). node(2,2). node(3,2).
node(1,3).            node(3,3).

start(1,(1,2)).
start(2,(3,2)).

goal(1,(3,2)).
goal(2,(1,2)).
