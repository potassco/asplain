%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Finds the hypothetical model using abduction

#defined _abduced/2.

:- _query(exclude,Atom), _model(hypothetical,Atom).
:- _query(include,Atom), not _model(hypothetical,Atom).

world(real;hypothetical).

{_abduced(X,Atom)} :- _abducible(X,Atom).

%=== Constraints

% (C1) No sense to remove something that is not in input
:- not _model(real,Atom), _abduced(rm,Atom).
% (C2) + (C4) No sense to both remove and add something
:- _abduced(add,Atom), _abduced(rm,Atom).
% (C3) No sense to add something that is already in input
:- _model(real,Atom), _abduced(add,Atom).

_model(hypothetical,Atom) :- _abduced(add, Atom).

%=== Distance

:~ _distance(N,D,L). [D@L,N]

% Default distance
% _distance((Atom,h), 1, 0) :- _model(hypothetical, Atom), not _model(real, Atom).
% _distance((Atom,r), 1, 0) :- _model(real, Atom), not _model(hypothetical, Atom).
