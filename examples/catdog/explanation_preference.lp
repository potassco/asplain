%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

_abducible((rm;add),assign(P,S)):-_model(real, person(P,_)),_model(real, seat(S)).

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
