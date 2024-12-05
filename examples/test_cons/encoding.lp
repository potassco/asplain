{sit;stand}.

% :- sit, stand.
% :- sit, stand.
% prevents(sit, (stand;laydown)).

c_ok(1):-not sit.
c_ok(1):-not stand.
:- not c_ok(1).

% ----- Assumptions
assumed(sit).
:- not sit, assumed(sit). % This is not working, is it
% :- not sit. % This is not working, is it
