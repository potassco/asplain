#include "./change.lp".

% EXTERNAL: path_depth(N).

% Always include query with distance 0
reachable_query(N,T) :- query(N, _), node(N,T).
% Always include changes with distance 0
reachable_change(N,T) :- change(_, N), node(N,T).

reachable_query(M,T) :- edge((N,M),_), node(M,T), reachable_query(N,_).
reachable_change(M,T) :- edge((N,M),_), node(M,T), reachable_change(N,_).

% FIND INTERSECTIONS

intersection(N,T) :- reachable_query(N,T), reachable_change(N,T).
reachable_query_back(N,T) :- intersection(N,T).
reachable_change_back(N,T) :- intersection(N,T).

% BACK DIRECTION

reachable_query_back(N,T) :- edge((N,M),_), node(N,T), reachable_query_back(M,_).
reachable_change_back(N,T) :- edge((N,M),_), node(N,T), reachable_change_back(M,_).

% PATH INCLUSIONS

node_path(N,T) :- reachable_query(N,T), reachable_query_back(N,T).
node_path(N,T) :- reachable_change(N,T), reachable_change_back(N,T).

% DEPTH

node_path_depth(N,T,0) :- node_path(N,T).
node_path_depth(M,T,D+1) :- node_path_depth(N,_,D), edge((N,M),_), node(M,T), path_depth(DMAX), D < DMAX.
node_path_depth(M,T,D+1) :- node_path_depth(N,_,D), edge((M,N),_), node(M,T), path_depth(DMAX), D < DMAX.

% INCLUDED

node_included(N,T) :- node_path_depth(N,T,D).
edge_included((N1,N2),T) :- edge((N1,N2),T), node_included(N1,_), node_included(N2,_).
