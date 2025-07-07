
% ## reduce
% Note: This is tricky to write since one holds is holds/2 and one is holds/1

% Penalize differences between the reference and the hypothetical model
_distance(Atom, 1, 1) :-
    hold(Atom,reference), not hold(Atom).

_distance(Atom, 1, 1) :-
    not hold(Atom,reference), hold(Atom).

% Penalize changes in the reason for a model
_distance(Reason, 1, 1) :-
    reason(Reason,reference), not reason(Reason).
