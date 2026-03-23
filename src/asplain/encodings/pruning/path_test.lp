#include "./abduced.lp".

% EXTERNAL: path_depth(N).

{node_path(N,T)} :- node(N,T).

reachable(N,T) :- query(N,_), node(N,T).
reachable(M,T) :- reachable(N,_), node_path(M,T), edge((N,M),_).
reachable(M,T) :- reachable(N,_), node_path(M,T), edge((M,N),_).

:- abduced(_,N), node(N,T), not reachable(N,T).

node_included(N,T) :- node_path(N,T).
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).



%#show .
%#show q(N) : reachable_query(N,_).
%#show a(N) : reachable_abduced(N,_).
