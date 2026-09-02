#include "./change.lp".

% Generate distance steps with the number of nodes being the maximum distance
%max_dist(D) :- D = #count{N: node(N,_)}.
max_dist(10).
dist(0..D) :- max_dist(D).

% Generate undirected edges
uedge(N,M) :- edge((N,M),_).
uedge(M,N) :- edge((N,M),_).

% REACHABILITY
% Start reachability from change nodes
reach(A,A,0) :- change(_,A).

% Reachability step with distance and cycle breaking
reach(N,O,D+1) :- reach(N,M,D), uedge(M,O), dist(D+1), not reach(N,O,D_BEFORE), dist(D_BEFORE), D_BEFORE < D+1.

% SHORTEST PATH
% Find best path from change nodes to queries
path(A,Q,D) :- reach(A,Q,D), change(_,A), query(Q,_).
path_shortest_dist(D_MIN) :- D_MIN = #min{D: path(A,Q,D)}.
path_shortest(A,Q,D) :- path(A,Q,D), path_shortest_dist(D).

% PATH BACKTRACKING
% Start shortest path backtracking
path_shortest_trace(Q,N,D-1) :- path_shortest(A,Q,D), uedge(Q,N), reach(A,N,D-1).

% Trace step for shortest path backtracking
path_shortest_trace(M,O,D-1) :- path_shortest(A,Q,_), path_shortest_trace(N,M,D), uedge(M,O), reach(A,O,D-1), D > 0.

% INCLUDE EDGES & NODES
% Select edges in both directions that match the trace edges and include their nodes
edge_included((M,O),T) :- path_shortest_trace(M,O,_), edge((M,O),T).
edge_included((O,M),T) :- path_shortest_trace(M,O,_), edge((O,M),T).
node_included(N,T) :- edge_included((N,_),_), node(N,T).
node_included(N,T) :- edge_included((_,N),_), node(N,T).
