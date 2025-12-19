
{removed(rule(H,B))}:-abducible(remove, rule(H,B)), node(reference, rule(H,B)).
{added(rule(H,B))}:-abducible(add, rule(H,B)), not node(reference, rule(H,B)).

% Nodes that are in the reference and not removed, plus added nodes
node(foil, R):- node(reference, R), not removed(R).
node(foil, R):- added(R).
% Edges that are in the reference and not removed, plus edges from added nodes
edge(foil, S, (X,Y)):-edge(reference, S, (X,Y)), not removed(X), not removed(Y).
edge(foil, S, (R,A)):-added(R), abducible(add, edge(S,(R,A))).
edge(foil, S, (R,A)):-added(R), abducible(add, edge(S,(A,R))).

% ------------------------------------------------
% # Check query

#defined query/2. % Comes from the input

fail_query:- query(Atom,exclude),  hold(atom(Atom)).
fail_query:- query(Atom,include), not hold(atom(Atom)).
:- fail_query.

% ------------------------------------------------
% # Preferred foil


%! cost(N, V, L). Cost of with name N value V and level L.
cost(default, 1, 1). % A default cost for each model with level 1 so that there is always some optimization
:~ cost(Name, Value, Level). [Value@Level, Name]
