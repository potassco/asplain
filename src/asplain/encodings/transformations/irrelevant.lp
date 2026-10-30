#include "change.lp".

relevant(N) :- node(N,_), tag(N,time(_)).
relevant(N) :- node(N,_), change(_,N).
relevant(N) :- node(N,_), fired(N).
relevant(N) :- node(N,_), query(N,_).

relevant(N1) :- edge((N1,N2),_), relevant(N2).

node_included(N,T)       :- node(N,T), relevant(N).
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
