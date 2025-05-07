% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% a inhibitor b: when a is true, b becomes false.
% a enabler of b: when a is true, b becomes true.

% Posioned if drinks d and not antidote a.
%   a acts as an inhibitor of p.
p :- d, not a.

% Antidote if not holiday h
%   h inhibitor of a, enabler of p.
% {h;w}.
% :- h, w.
% :- not h, not w.
1{h;w}1.

a :- w.
a :- s.

d. s.
% {f}.
% :- h, not f.
% :- f, not h.
% p:-f.



% p:- stupid.
% stupid.

% p:- not cleaver.

% #external cleaver.


% a:- b.

% {b}.
% Bond drinks d and is not on a holiday.
% d.
% h.
% p.
% a :- p, h.
% a:-d.
% b:- p, h.
% 4{a(1..5)}4.

% c.
% c:-d.
% d.
% {e}.

% :- not 3 #sum{1,a(X):a(X)}.
% {a(1..5)}.
% a(1..3).
% Only model {d, h, p}
