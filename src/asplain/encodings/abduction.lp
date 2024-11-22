%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% _model(real,Atom)
% Atom is obtained by solving the program as it was given.
% What is in input, is assumed to be naturally true
% What is not in input, is assumed to be naturally false

% hypothetical(Atom)
% Atom is true/false in the hypothetical world we are
% reasoning about. The certainty/falsety of the atom
% may come from what is natural or from the
% assumptions we may make in the hypothetical world.

#defined _abduced/2.

:- _query(exclude,Atom), _model(hypothetical,Atom).
:- _query(include,Atom), not _model(hypothetical,Atom).

world(real;hypothetical).

{_abduced(X,Atom)} :- _abducible(X,Atom).

% Constraints
% (C1) No sense to remove something that is not in input
:- not _model(real,Atom), _abduced(rm,Atom).
% (C2) + (C4) No sense to both remove and add something
:- _abduced(add,Atom), _abduced(rm,Atom).
% (C3) No sense to add something that is already in input
:- _model(real,Atom), _abduced(add,Atom).

_model(hypothetical,Atom) :- _abduced(add, Atom).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:~ _distance(N,D,L). [D@L,N]

% Default distance
% _distance((Atom,h), 1, 0) :- _model(hypothetical, Atom), not _model(real, Atom).
% _distance((Atom,r), 1, 0) :- _model(real, Atom), not _model(hypothetical, Atom).
