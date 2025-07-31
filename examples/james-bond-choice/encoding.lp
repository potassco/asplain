% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% a inhibitor b: when a is true, b becomes false.
% a enabler of b: when a is true, b becomes true.

% Posioned if drinks d and not antidote a.
%   a acts as an inhibitor of p.
p :- d, not a, &tag_rule{nl("Bond is poisoned if he drinks the drug and does not receive the antidote.",())}.

% Holiday or work day.
{h;w}:- &tag_rule{nl("Bond is either on holiday or working.",())}.
:- h, w, &tag_rule{nl("Bond cannot be both on holiday and working.",())}.
:- not h, not w, &tag_rule{nl("Bond has to be either on holiday or working.",())}.
% 1{h;w}1.

% Antidote if work day
a :- w, &tag_rule{nl("Bond receives the antidote if he is working.",())}.

% Extra to have multiple reasons for antidote.
% Antidote if smart.
a :- s, &tag_rule{nl("Bond receives the antidote if he is smart.",())}.


%==== Instance
d:- &tag_rule{abducible(rm)}, &tag_rule{input}.
s:- &tag_rule{abducible(add)}, &tag_rule{disabled}, &tag_rule{input}.


% :- a, not &tag_atom{nl("Bond has received the antidote.",())}.
% :- d, not &tag_atom{nl("Bond has drunk the drug.",())}.
% :- p, not &tag_atom{nl("Bond has been poisoned.",())}.
% :- h, not &tag_atom{nl("Bond is on holiday.",())}.
% :- w, not &tag_atom{nl("Bond is working.",())}.
% :- s, not &tag_atom{nl("Bond is smart.",())}.
% #external s.

% :-d.
