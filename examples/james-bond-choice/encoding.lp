% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% Input
% @label("Bond has drunk the drug") :: d
% @label("Bond has received the antidote") :: a
% @label("Bond is on holiday") :: h
% @label("Bond is working") :: w


% @label("Bond might be holiday or working")
{h;w}.
% @label("Bond has to be either on holiday or working")
:- not h, not w.
% @label("Bond cannot be both on holiday and working")
:- h, w.


% @label("Bond receives the antidote if he is working")
a :- w.
% @label("Bond is poisoned if he drinks the drug and does not receive the antidote")
p :- d, not a.

d.
