
{removed(R)}:-optional(remove, R), program(R, ref).
{added(R)}:-optional(add, R), not program(R, ref).

% Nodes that are in the reference and not removed, plus added nodes
program(N, foil):- program(N, ref), not removed(N).
program(R, foil):- added(R).

% ------------------------------------------------
% # Check query

#defined query/2. % Comes from the input

% Classify temporal queries
temporal(temporal(Q,T)) :- query(temporal(Q,T),_).

% Normal queries
:- query(A,0), not temporal(A), model(A, foil).
:- query(A,1), not temporal(A), not model(A, foil).

% Temporal queries
:- query(temporal(Q,T),0), holds(Q,T).
:- query(temporal(Q,T),1), not holds(Q,T).

% ------------------------------------------------
% # Temporal operators over fluents in foil

used(Q) :- query(temporal(Q,T),_).
used(Q) :- used(neg(Q)).
used(Q) :- used(con(Q,_)).
used(Q) :- used(con(_,Q)).
used(Q) :- used(dis(Q,_)).
used(Q) :- used(dis(_,Q)).
used(Q) :- used(x(Q)).
used(Q) :- used(p(Q)).
used(Q) :- used(g(Q)).
used(Q) :- used(f(Q)).
used(Q) :- used(u(Q,_)).
used(Q) :- used(u(_,Q)).
used(Q) :- used(s(Q,_)).
used(Q) :- used(s(_,Q)).

t(T) :- model(time(T), foil).
holds(F,T) :- used(F), t(T), model(holds(F,T), foil).                                                    % Fluent F holds at T
holds(dis(F,G),T) :- used(dis(F,G)), t(T), holds(G,T).                                                   % (C) Or
holds(dis(F,G),T) :- used(dis(F,G)), t(T), holds(F,T).                                                   % (C) Or
holds(con(F,G),T) :- used(con(F,G)), t(T), holds(F,T), holds(G,T).                                       % (C) And
holds(neg(F),T) :- used(neg(F)), t(T), not holds(F,T).                                                   % (C) Not
holds(x(F),T) :- used(x(F)), t(T), t(T+1), holds(F,T+1).                                                 % (T) Next
holds(p(F),T) :- used(p(F)), t(T), t(T-1), holds(F,T-1).                                                 % (T) Previous
holds(g(F),T) :- used(g(F)), t(T), holds(F,I) : t(I), I >= T.                                            % (T) Always
holds(f(F),T) :- used(f(F)), t(T), t(I), holds(F,I), I >= T.                                             % (T) Eventually
holds(u(F,G),T) :- used(u(F,G)), t(T), t(T'), T <= T', holds(G,T'), holds(F,I): t(I), T <= I, I < T'.    % (T) Until
holds(s(F,G),T) :- used(s(F,G)), t(T), t(T'), T >= T', holds(G,T'), holds(F,I): t(I), T' < I, I <= T.    % (T) Since

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
