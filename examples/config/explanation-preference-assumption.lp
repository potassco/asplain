% %%% _abducible(A)
% % A is an abducible atom
% % If A is true in the model then it may be removed for the contrastive explanation.
% % If A is false in the model then it may be added for the contrastive explanation


distance(Atom, 1, 2) :-
    abduced(_, Atom), _input(Atom).
distance(Atom, 1, 1) :-
    abduced(_, Atom), not _input(Atom).

% --- General code for assumptions
_abducible((rm;add),X):-_input(X).
:- _input(X), not _model(hypothetical, X), not abduced(rm, X).
