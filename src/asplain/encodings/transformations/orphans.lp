#include "./change.lp".

% Always include query
node_included(N,T) :- query(N, _), node(N,T).
% Always include changes
node_included(N,T) :- change(_, N), node(N,T).

node_included(N2,T) :- node_included(N1,_), node(N2,T), edge((N1,N2), _).
node_included(N2,T) :- node_included(N1,_), node(N2,T), edge((N2,N1), _).

edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
