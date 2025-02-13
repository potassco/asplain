% #const reachable=true.
#const reachable=false.

reachable(node,A):-reachable!=true, node(A).
reachable(edge,ID):-reachable!=true, edge(X,Y,ID).

reachable(node,A):-reachable=true, attr(node,A,abduced,X).
reachable(node,A):-reachable=true, attr(node,A,query,X).
reachable(edge,ID):-reachable=true, edge(Cause, Effect, ID), reachable(node, Effect).
reachable(node,Cause):-reachable=true, edge(Cause, Effect, ID), reachable(node, Effect).
