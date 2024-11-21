%===== Abducibles
_xclingo_abducible((rm;add),d).
_xclingo_abducible((rm;add),h).

%===== Distance
_xclingo_distance(Atom, 1, 1) :-
    _xclingo_abduced(_, Atom).

%===== Reference model
_xclingo_model(real,d).
_xclingo_model(real,p).
_xclingo_model(real,h).

%===== Query
:- _xclingo_model(hypothetical,p).  % can't be that is poisoned

%===== Shown
_xclingo_show_trace(W, A) :- _xclingo_model(W,A).
