#include "change.lp".

% Always include query
node_included(N,T) :- query(N,_), node(N,T).

% Always include changes & fired constraints
node_included(N,T) :- node(N,T), change(_,N).
node_included(N,T) :- node(N,T), fired(N).

% Include nodes that are either in the foil or ref model
node_included(N,T) :- node(N,T), model(N,_).

% Include edges between included nodes
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
