% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

% _abducible((rm;add),d).
% _abducible((rm;add),h).

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

_distance(Atom, 1, 3) :-
    _abduced(_, Atom).


% !!! warning
%        This is tricky to write since reference model uses holds/2 and reason/2,
%        while for the hypothetical it uses holds/1 and reason/1.

% Penalty for changing the reason of an atom
_distance(Reason, 1, 2) :-
    reason(Reason,reference), not reason(Reason).


% The following distance produces a single optimal explanation by removing the one where h is added.
% _distance(Atom, 1, 1) :-
%     hold(Atom,reference), not hold(Atom).

% _distance(Atom, 1, 1) :-
%     not hold(Atom,reference), hold(Atom).
