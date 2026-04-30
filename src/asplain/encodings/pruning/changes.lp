#include "./abduced.lp".

% Always include query
node_included(N,T) :- query(N, _), node(N,T).
% Always include abductions
node_included(N,T) :- abduced(_, N), node(N,T).
node_included(N,T) :- fired(N), node(N,T).

node_included(N,T) :- node(N, T), model(N, ref), not model(N, foil).
node_included(N,T) :- node(N, T), model(N, foil), not model(N, ref).

edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
