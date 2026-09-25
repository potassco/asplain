#include "change.lp".

% Always include query
node_included(N,T) :- query(N,_), node(N,T).

% Always include changes & fired constraints
node_included(N,T) :- node(N,T), change(_,N).
node_included(N,T) :- node(N,T), fired(N).

% Find fact nodes which are in both models
fact(N) :- node(N,atom), not edge((_,N),_), model(N,ref), model(N,foil).
% Include nodes if they are non-timed facts
node_included(N,T) :- node(N,T), not fact(N).
node_included(N,T) :- node(N,T), fact(N), tag(N,time(_)).

% Include edges between included nodes
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
