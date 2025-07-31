%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

% _abducible((rm;add),assign(P,S)):-node(atom(person(P,_))),node(atom(seat(S))).

distance(Atom, 1, 1) :-
    abduced(_, Atom).


% ## reduce
% This is tricky to write since one holds in holds/2 and one is holds/1
distance(Atom, 1, 1) :-
    used_to_hold(Atom), not hold(Atom).

distance(Atom, 1, 1) :-
    not used_to_hold(Atom), hold(Atom).

distance(Reason, 1, 1) :-
    reason(Reason,reference), not reason(Reason).
