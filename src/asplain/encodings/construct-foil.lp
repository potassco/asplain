
{removed(R)}:-abducible(remove, R), program(R, ref).
{added(R)}:-abducible(add, R), not program(R, ref).

% Nodes that are in the reference and not removed, plus added nodes
program(N, foil):- program(N, ref), not removed(N).
program(R, foil):- added(R).

% ------------------------------------------------
% # Check query

#defined query/2. % Comes from the input

:- query(A,0),  model(A, foil).
:- query(A,1), not model(A, foil).

% ------------------------------------------------
% # Preferred foil

%! cost(N, V, L). Cost of with name N value V and level L.
cost(default, 1, 1). % A default cost for each model with level 1 so that there is always some optimization
:~ cost(Name, Value, Level). [Value@Level, Name]

%  -----------

some_model(1, A) :- node(A,atom), #count{W: model(A,W)}>=1.
some_model(0, A) :- node(A,atom), #count{W: model(A,W)}<=1.

fired(R):- node(R, rule(disjunction)), #false : edge((R,A),_);
           some_model(T, A): edge((A,R),T).
