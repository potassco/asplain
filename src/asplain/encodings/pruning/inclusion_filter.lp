% Filtered
program_included(N,P) :- node_included(N,_), program(N,P).
abducible_included(A,N) :- node_included(N,_), abducible(A,N).
model_included(N,M) :-  node_included(N,_), model(N,M).
tag_included(N,T) :- node_included(N,_), tag(N,T).

% Not Filtered
query_included(N,Q) :- query(N,Q).
solved_included(S) :- solved(S).



#show .
#show node(N,T) : node_included(N,T).
#show edge(E,T) : edge_included(E,T).

#show program(N,P) : program_included(N,P).
#show abducible(A,N) : abducible_included(A,N).
#show model(N,M) : model_included(N,M).
#show tag(N,T) : tag_included(N,T).
#show query(N,Q) : query_included(N,Q).
#show solved(S) : solved_included(S).
