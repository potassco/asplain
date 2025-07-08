% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% a inhibitor b: when a is true, b becomes false.
% a enabler of b: when a is true, b becomes true.

% Posioned if drinks d and not antidote a.
%   a acts as an inhibitor of p.
p :- d, not a.

% Holiday or work day.
{h;w}.
:- h, w.
:- not h, not w.
% 1{h;w}1.

% Antidote if work day
a :- w.
d. %<- abducible

% Extra to have multiple reasons for antidote.
% Antidote if smart.
a :- s.
% s. %<- abducible


% Mimic users assumptions
:- not h. % Assume h is true, i.e., Bond is on holiday. Works only with explanation_preference.lp


#external s.
