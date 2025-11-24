
% ## reduce
% Note: This is tricky to write since one holds is holds/2 and one is holds/1

% Penalize differences between the reference and the hypothetical model
distance(Atom, 1, 1) :-
    used_to_hold(Atom), not hold(Atom).

distance(Atom, 1, 1) :-
    not used_to_hold(Atom), hold(Atom).

% Penalize changes in the reason for a model
% distance(Reason, 1, 1) :-
    % reason(Reason,reference), not reason(Reason).
