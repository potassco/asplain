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
a :- not h.

% Bond drinks d and is not on a holiday.
d.
{h}.

% Only model {d, h, p}
