
% Makes sure that the query holds in the hypothetical model.
#defined query/2. % Comes from the input

fail_query:- query(exclude,Atom),  hold(atom(Atom)).
fail_query:- query(include,Atom), not hold(atom(Atom)).
