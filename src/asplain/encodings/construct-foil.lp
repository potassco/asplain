
{removed(R)}:-tag(reference, R, abducible(remove)).
{added(R)}:-tag(reference, R, abducible(add)).


node(foil, X):-node(reference, X), not removed(X).
tag(foil, X, disabled):- tag(reference, X, disabled), not added(X).
edge(foil, S, (X,Y)):-edge(reference, S, (X,Y)), not removed(X), not removed(Y).

% ------------------------------------------------
% # Check query

#defined _query/2. % Comes from the input

fail_query:- _query(Atom,exclude),  hold(atom(Atom)).
fail_query:- _query(Atom,include), not hold(atom(Atom)).
:- fail_query.

% ------------------------------------------------
% # Preferred foil


%! cost(N, V, L). Cost of with name N value V and level L.
cost(default, 1, 1). % A default cost for each model with level 1 so that there is always some optimization
:~ cost(Name, Value, Level). [Value@Level, Name]
