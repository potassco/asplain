% Penalize more abducing something that is not an input
% Note: works with util_preferences/assumptions_as_input.lp

_distance(A, 1, 1) :-
    _chance_input(_, A), _input(A,_).
_distance(A, 1, 2) :-
    _chance_input(_, A), not _input(A,_).
