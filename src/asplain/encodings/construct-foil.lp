% Choice rule to allow all removables and addables to be changed

{removed(R)}:-optional(remove, R), program(R, ref).
{added(R)}:-optional(add, R), not program(R, ref).

% Assert program nodes
program(N, foil):- program(N, ref), not removed(N).
program(R, foil):- added(R).

% Enforce the query atoms appear in the foil model

#defined query/2.

:- query(A,0),  model(A, foil).
:- query(A,1), not model(A, foil).

%  Define a default cost for each model with level `1` so that there is always some optimization.
% `cost(N, V, L)` represents cost with name `N`, value `V` and level `L`.
cost(default, 1, 1).
:~ cost(Name, Value, Level). [Value@Level, Name]

% Assert if an atom node appears in some model

some_model(1, A) :- node(A,atom), #count{W: model(A,W)}>=1.
some_model(0, A) :- node(A,atom), #count{W: model(A,W)}<=1.

% Assert all rule nodes that derrive an atom that is in some model as fired

fired(R):- node(R, rule(disjunction)), #false : edge((R,A),_);
           some_model(T, A): edge((A,R),T).
