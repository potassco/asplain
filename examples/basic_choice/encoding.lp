%
% The running example from the paper
% Alviano et.al., "Answer Set Explanations via Preferred Unit-Provable Unsatisfiable Subsets"
%

p(X) :- s(X,Y), not r(Y).

% choice rule with boundries have been manually transformed
{ r(a); r(b) }.
:- not r(a), not r(b).
:- r(a), r(b).

s(a,b).
s(b,a).
