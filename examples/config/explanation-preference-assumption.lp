% %%% _abducible(A)
% % A is an abducible atom
% % If A is true in the model then it may be removed for the contrastive explanation.
% % If A is false in the model then it may be added for the contrastive explanation


_distance(Atom, 1, 2) :-
    _abduced(_, Atom), _input(Atom).
_distance(Atom, 1, 1) :-
    _abduced(_, Atom), not _input(Atom).

% --- General code for assumptions
_abducible((rm;add),X):-_input(X).
:- _input(X), not _model(hypothetical, X), not _abduced(rm, X).
