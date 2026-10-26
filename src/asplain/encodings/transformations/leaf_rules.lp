#include "change.lp".

% Always include query
node_included(N,T) :- query(N,_), node(N,T).

% Always include changes & fired constraints
node_included(N,T) :- node(N,T), change(_,N).
node_included(N,T) :- node(N,T), fired(N).

% Find dead end rule nodes which are not constraints
rule_dead_end(N,rule(R)) :- node(N,rule(R)), not tag(N,constraint), not edge((N,_),_).

% Only include nodes that are not dead ends or have incoming edges
node_included(N,T) :- node(N,T), not rule_dead_end(N,T).

% Include edges between included nodes
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
