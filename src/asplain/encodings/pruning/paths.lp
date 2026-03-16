#include "./abduced.lp".

% Always include query with distance 0
reachable_query(N,T) :- query(N, _), node(N,T).
% Always include abductions with distance 0
reachable_abduced(N,T) :- abduced(_, N), node(N,T).

reachable_query(N,T) :- edge((N,M),_), node(N,T), reachable_query(M,_).
reachable_abduced(M,T) :- edge((N,M),_), node(M,T), reachable_abduced(N,_).

node_included(N,T) :- reachable_query(N,T), reachable_abduced(N,T).

edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
