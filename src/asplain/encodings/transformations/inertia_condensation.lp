% Condense inertia chains into single edges

inertia_node(N,T) :- node(N,T), tag(N,inertia).
inertia_edge((IN,OUT),T) :- inertia_node(N,_), edge((IN,N),T), edge((N,OUT),T), IN=holds(_,_).

% start inertia chain at first inertia edge
chain_((N,M),T) :- inertia_edge((N,M),T), not inertia_edge((_,N),T).
% extend inertia chain with next inertia edge
chain_((N,O),T) :- chain_((N,M),T), inertia_edge((M,O),T).
% inertia chain is complete
chain((N,M),T) :- chain_((N,M),T), not inertia_edge((M,_),T).

edge_excluded((N,M),T) :- inertia_edge((N,M),T).                       % exclude inertia edges
node_excluded(N,T) :- inertia_node(N,T).                               % exclude inertia nodes
node_excluded(N,T) :- chain_((_,N),_), node(N,T), not chain((_,N),_).  % exclude intermediate chain nodes


edge_included((N,M),T) :- chain((N,M),T).
edge_tag((N,M),inertia_condensed) :- chain((N,M),_).

node_included(N,T) :- node(N,T), not node_excluded(N,T).
edge_included((N,M),T) :- edge((N,M),T), not edge_excluded((N,M),T).
