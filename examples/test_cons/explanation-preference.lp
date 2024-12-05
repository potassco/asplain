% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

_abducible((rm;add),sit).
_abducible((rm;add),stand).

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).

% _direct_inhibitor(2, real, sit, stand).
% _direct_inhibitor(2, hypothetical, stand, sit).
