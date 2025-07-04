% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

_abducible((rm;add),d).
_abducible((rm;add),s).

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

% Abduce the least models
_distance(Atom, 1, 3) :-
    _abduced(_, Atom).


% ## reduce
% Note: This is tricky to write since one holds in holds/2 and one is holds/1

% Penalize differences between the reference and the hypothetical model
% _distance(Atom, 1, 1) :-
%     hold(Atom,reference), not hold(Atom).

% _distance(Atom, 1, 1) :-
%     not hold(Atom,reference), hold(Atom).

% % Penalize changes in the reason for a model
% _distance(Reason, 1, 1) :-
%     reason(Reason,reference), not reason(Reason).
