%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

_abducible((rm;add),assign(P,S)):-node(atom(person(P,_))),node(atom(seat(S))).

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).


% ## reduce
% This is tricky to write since one holds in holds/2 and one is holds/1
_distance(Atom, 1, 1) :-
    hold(Atom,reference), not hold(Atom).

_distance(Atom, 1, 1) :-
    not hold(Atom,reference), hold(Atom).

_distance(Reason, 1, 1) :-
    reason(Reason,reference), not reason(Reason).
