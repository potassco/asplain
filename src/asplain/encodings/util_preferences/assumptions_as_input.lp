% --- General code for assumptions treated directly in the preference
% This gives us the flexibility of not having to change the program graph and treating them differently

{_abduce_input(add,X)}:-_input(X,false).
{_abduce_input(rm,X)}:-_input(X,true).

% Force input in the hypothetical model unless it is abduced
:- _input(X,true), not hold(X), not _abduce_input(rm, X).
:- _input(X,false),  hold(X), not _abduce_input(add, X).

% Force input in the reference model
:- _input(X,true), not hold(X,reference).
:- _input(X,false),  hold(X,reference).

% Goes in hand with the distance in util_distance/prefer_abduce_input.lp
