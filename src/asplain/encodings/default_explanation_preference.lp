%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

_abducible((rm;add),Atom) :- _sup(R, W, Atom, Vars), not _depends(_sup(R, W, _, _), _), not _prevents(_sup(R, W, _, _), _).

% Issue: this only captures atoms that were written as facts in the program. So it only consider to remove those, and not to add new ones.

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
