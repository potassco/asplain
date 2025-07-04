% %%% _abducible(A)
% % A is an abducible atom
% % If A is true in the model then it may be removed for the contrastive explanation.
% % If A is false in the model then it may be added for the contrastive explanation

_abducible((rm;add),d).
_abducible((rm;add),s).

% Penalize more abducing something that is not an input
_distance(Atom, 1, 1) :-
    _abduced(_, Atom), _input(Atom,_).
_distance(Atom, 1, 2) :-
    _abduced(_, Atom), not _input(Atom,_).

% Penalize any abduction equally
% _distance(Atom, 1, 3) :-
%     _abduced(_, Atom).

% --- General code for assumptions
_abducible(rm,X):-_input(X,true).
_abducible(add,X):-_input(X,false).
:- _input(X,true), not hold(X), not _abduced(rm, X).
:- _input(X,false),  hold(X), not _abduced(add, X).

:- _input(X,true), not hold(X,reference).
:- _input(X,false),  hold(X,reference).

_input(h,true).

#show _input/2.
