% Condense inertia chains into single edges

worlds(ref;foil;both).

% Identify inertia rule nodes
inertia_node_(IR,F,(IN,OUT)) :- node(IR,rule(disjunction)), edge((IN,IR),1), edge((IR,OUT),1), IN=holds(F,T1), OUT=holds(F,T2).
% Check if an inertia node has other incoming edges
other_incoming(IR) :- inertia_node_(IR,_,(IN,_)), edge((OTHER,IR),_), OTHER != IN.

% Create inertia node facts with the covered worlds if there are no other incoming edges
inertia_node(IR,F,both,(IN,OUT)) :- inertia_node_(IR,F,(IN,OUT)), not other_incoming(IR), model(IR,ref), model(IR,foil).
inertia_node(IR,F,ref,(IN,OUT)) :- inertia_node_(IR,F,(IN,OUT)), not other_incoming(IR), model(IR,ref), not model(IR,foil).
inertia_node(IR,F,foil,(IN,OUT)) :- inertia_node_(IR,F,(IN,OUT)), not other_incoming(IR), not model(IR,ref), model(IR,foil).

% Identify uniform inertia chains
chain_(F,W,(IN,OUT)) :- inertia_node(IR,F,W,(IN,OUT)), not inertia_node(_,F,W,(_,IN)).
chain_(F,W,(IN,NEXT)) :- chain_(F,W,(IN,OUT)), inertia_node(_,F,W,(OUT,NEXT)).
chain(F,W,(IN,OUT)) :- chain_(F,W,(IN,OUT)), not inertia_node(_,F,W,(OUT,_)).

% Include uniform inertia chain edges
edge_included((IN,OUT),1) :- chain(_,_,(IN,OUT)).
edge_tag((IN,OUT),inertia_condensed) :- chain(_,_,(IN,OUT)).

% Exclude uncondensed inertia edges
edge_excluded((IN,IR),T) :- inertia_node(IR,_,_,_), edge((IN,IR),T).                     % inertia edges incoming
edge_excluded((IR,OUT),T) :- inertia_node(IR,_,_,_), edge((IR,OUT),T).                   % inertia edges outgoing
node_excluded(IR,rule(disjunction)) :- inertia_node(IR,_,_,_).                           % rule nodes
node_excluded(OUT,atom) :- chain_(_,_,(_,OUT)), node(OUT,atom), not chain(_,_,(_,OUT)).  % fluent nodes

node_included(N,T) :- node(N,T), not node_excluded(N,T).
edge_included((N,M),T) :- edge((N,M),T), not edge_excluded((N,M),T).
