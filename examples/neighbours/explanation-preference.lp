% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

_distance(Atom, 1, 2) :-
    _abduced(_, Atom), _input(Atom).
_distance(Atom, 1, 1) :-
    _abduced(_, Atom), not _input(Atom).

_abducible((add;rm),X) :- _input(_,X).
:- _input(add,X), not _model(hypothetical, X), not _abduced(rm, X).

_domain(color(C)) :- _model(real,color(C)).
_domain(house(H)) :- _model(real,house(H)).