% Generate distance steps with the number of nodes being the maximum distance
max_dist(D) :- D = #count{N: node(N)}.
dist(0..D) :- max_dist(D).

% Generate undirected edges
uedge(N,M) :- edge(N,M).
uedge(M,N) :- edge(N,M).

% REACHABILITY
% Start reachability from abduced nodes
reach(N,N,0) :- abduced(N).

% Reachability step with distance and cycle breaking
reach(N,O,D+1) :- reach(N,M,D), uedge(M,O), dist(D+1), not reach(N,O,D_BEFORE), dist(D_BEFORE), D_BEFORE < D+1.

% SHORTEST PATH
% Find best path from abduced nodes to queries
path(A,Q,D) :- reach(A,Q,D), abduced(A), query(Q).
path_shortest_dist(D_MIN) :- D_MIN = #min{D: path(A,Q,D)}.
path_shortest(A,Q,D) :- path(A,Q,D), path_shortest_dist(D).

% PATH BACKTRACKING
% Start shortest path backtracking
path_shortest_trace(Q,N,D-1) :- path_shortest(A,Q,D), uedge(Q,N), reach(A,N,D-1).

% Trace step for shortest path backtracking
path_shortest_trace(M,O,D-1) :- path_shortest(A,Q,_), path_shortest_trace(N,M,D), uedge(M,O), reach(A,O,D-1), D > 0.

#show path_shortest_trace/3.
