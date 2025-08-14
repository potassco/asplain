% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% a inhibitor b: when a is true, b becomes false.
% a enabler of b: when a is true, b becomes true.

% Posioned if drinks d and not antidote a.
%   a acts as an inhibitor of p.
p :- d, not a, &tag_rule{nl("Bond is poisoned if he drinks the drug and does not receive the antidote.",())}.

% Holiday or work day.
% 1{h;w}1:- &tag_rule{nl("Bond might be holiday or working.",())}.
% {h}:- &tag_rule{nl("Bond might be holiday or working.",())}.
% {w}:- &tag_rule{nl("Bond might be holiday or working.",())}.
% :- not #sum{1,h:h;1,w:w}=1, &tag_rule{nl("Bond has to be either on holiday or working.",())}.
{h;w}:- &tag_rule{nl("Bond might be holiday or working.",())}.
:- h, w, &tag_rule{nl("Bond cannot be both on holiday and working.",())}.
:- not h, not w, &tag_rule{nl("Bond has to be either on holiday or working.",())}.
% x1:-w, &tag_rule{nl("Bond is working 1.",())}.
% x2:-x1, &tag_rule{nl("Bond is working 2.",())}.
% :- h, x2, &tag_rule{nl("Bond cannot be both on holiday and working.",())}.
% :- not h, not x2, &tag_rule{nl("Bond has to be either on holiday or working.",())}.
% h :- not w, &tag_rule{nl("Bond is on holiday if not working.",())}.
% w :- not h, &tag_rule{nl("Bond is working if not on holiday.",())}.



% 1{h;w}1:-&tag_rule{nl("Bond has to be either on holiday or working.",())}.

% Antidote if work day
a :- w, &tag_rule{nl("Bond receives the antidote if he is working.",())}.

% Extra to have multiple reasons for antidote.
% Antidote if smart.
a :- s, &tag_rule{nl("Bond receives the antidote if he is smart.",())}.


%==== Instance
d:- &tag_rule{abducible(rm)}.
s:- &tag_rule{abducible(add)}, &tag_rule{disabled}.


% :- a, not &tag_atom{nl("Bond has received the antidote.",())}.
% :- d, not &tag_atom{nl("Bond has drunk the drug.",())}.
% :- p, not &tag_atom{nl("Bond has been poisoned.",())}.
% :- h, not &tag_atom{nl("Bond is on holiday.",())}.
% :- w, not &tag_atom{nl("Bond is working.",())}.
% :- s, not &tag_atom{nl("Bond is smart.",())}.
% #external s.

% :-d.
