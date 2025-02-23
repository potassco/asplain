
_distance(default, 1, 999).

_distance(Atom, 1, 3) :-
    _abduced(_, Atom), _input(Atom).
_distance(Atom, 1, 2) :-
    _abduced(_, Atom), not _input(Atom).
_distance(Atom, 1, 1) :-
    _model(real, Atom), not _model(hypothetical, Atom).
_distance(Atom, 1, 1) :-
    _model(hypothetical, Atom), not _model(real, Atom).

% --- General code for assumptions
_abducible(rm, X):- _input(X).
_abducible(rm, initial(X,Y,V)) :- _model(real, initial(X,Y,V)).

:- _input(X), not _model(hypothetical, X), not _abduced(rm, X).
