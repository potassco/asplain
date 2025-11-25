
{removed(R)}:-tag(reference, R, abducible(remove)).
{added(R)}:-tag(reference, R, abducible(add)).


node(graph, X):-node(reference, X), not removed(X).
tag(graph, X, disabled):- tag(reference, X, disabled), not added(X).
edge(graph, S, (X,Y)):-edge(reference, S, (X,Y)), not removed(X), not removed(Y).

% ------------------------------------------------
% # Check query

#defined _query/2. % Comes from the input

fail_query:- _query(Atom,exclude),  hold(atom(Atom)).
fail_query:- _query(Atom,include), not hold(atom(Atom)).
:- fail_query.

% TODO distance
