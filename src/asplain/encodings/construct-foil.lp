
{removed(R)}:-abducible(remove, R), program(R, ref).
{added(R)}:-abducible(add, R), not program(R, ref).

% Nodes that are in the reference and not removed, plus added nodes
program(N, foil):- program(N, ref), not removed(N).
program(R, foil):- added(R).

% Edges that are in the reference and not removed, plus edges from added nodes
% edge(foil, S, (X,Y)):-edge((X,Y)), not removed(X), not removed(Y).
% edge(foil, S, (R,A)):-added(R), abducible(add, edge(S,(R,A))).
% edge(foil, S, (A,R)):-added(R), abducible(add, edge(S,(A,R))).

% ------------------------------------------------
% # Check query

#defined query/2. % Comes from the input

fail_query:- query(A,exclude),  model(A, foil).
fail_query:- query(A,include), not model(A, foil).
:- fail_query.

% ------------------------------------------------
% # Preferred foil

%! cost(N, V, L). Cost of with name N value V and level L.
cost(default, 1, 1). % A default cost for each model with level 1 so that there is always some optimization
:~ cost(Name, Value, Level). [Value@Level, Name]

%  -----------

some_model(1, A) :- node_type(A,atom), #count{W: model(A,W)}>=1.
some_model(0, A) :- node_type(A,atom), #count{W: model(A,W)}<=1.

fired(R):- node_type(R, rule(disjunction)), #false : edge((R,A));
           some_model(T, A): edge_type((A,R),T).
