%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

% _abducible((rm;add),alcohol(clare)).
% _abducible((rm;add),alcohol(gabriel)).

% _abducible((rm;add),resist(clare)).
% _abducible((rm;add),resist(gabriel)).

_abducible((rm;add), paid_taxes). 

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
