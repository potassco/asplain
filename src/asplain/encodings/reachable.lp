#const reachable=false.

reachable(node,A):-reachable!=true, node(A).
reachable(edge,ID):-reachable!=true, edge(X,Y,ID).

% reachable(node,A):-reachable=true, attr(node,A,abduced,X).
reachable(from,node,A):-reachable=true, attr(node,A,abduced,X).
reachable(to,node,A):-reachable=true, attr(node,A,query,X).

reachable(to,edge,ID):-reachable=true, edge(Cause, Effect, ID), reachable(to, node, Effect),not _domain(Effect).
reachable(to,node,Cause):-reachable=true, edge(Cause, Effect, ID), reachable(to, node, Effect),not _domain(Effect).

reachable(from,edge,ID):-reachable=true, edge(Cause, Effect, ID), reachable(from, node, Cause),not _domain(Cause).
reachable(from,node,Effect):-reachable=true, edge(Cause, Effect, ID), reachable(from, node, Cause),not _domain(Cause).


reachable(T,V):-reachable==true, reachable(_,T,V).
