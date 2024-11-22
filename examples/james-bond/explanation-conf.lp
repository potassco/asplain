%===== Abducibles
_abducible((rm;add),d).
_abducible((rm;add),h).

%===== Distance
_distance(Atom, 1, 1) :-
    _abduced(_, Atom).

%===== Reference model
_model(real,d).
_model(real,p).
_model(real,h).

%===== Query
:- _model(hypothetical,p).  % can't be that is poisoned

%===== Shown
_show_trace(W, A) :- _model(W,A).
