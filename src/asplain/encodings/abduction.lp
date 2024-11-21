%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% _xclingo_model(real,Atom)
% Atom is obtained by solving the program as it was given.
% What is in input, is assumed to be naturally true
% What is not in input, is assumed to be naturally false

% hypothetical(Atom)
% Atom is true/false in the hypothetical world we are
% reasoning about. The certainty/falsety of the atom
% may come from what is natural or from the
% assumptions we may make in the hypothetical world.

#defined _xclingo_abduced/2.

world(real;hypothetical).

{_xclingo_abduced(X,Atom)} :- _xclingo_abducible(X,Atom).

% Constraints
% (C1) No sense to remove something that is not in input
:- not _xclingo_model(real,Atom), _xclingo_abduced(rm,Atom).
% (C2) + (C4) No sense to both remove and add something
:- _xclingo_abduced(add,Atom), _xclingo_abduced(rm,Atom).
% (C3) No sense to add something that is already in input
:- _xclingo_model(real,Atom), _xclingo_abduced(add,Atom).

_xclingo_model(hypothetical,Atom) :- _xclingo_abduced(add, Atom).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:~ _xclingo_distance(N,D,L). [D@L,N]
