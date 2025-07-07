% Abducible rules from an atom definition
% The preference input: _abducible(_,A) with A an atom adds the possibility of adding or removing A as a fact.
_abducible_rule(rm, rule(H,B)):- _abducible(rm,A),
                    _fact(rule(H,B)),
                    edge((rule(H,B), atom(A)),reference).

_abducible_rule(add, rule(disjunction(added(A)),normal(A))):- _abducible(add,A),
                    node(atom(A)).
