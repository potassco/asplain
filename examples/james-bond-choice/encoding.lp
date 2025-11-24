% If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
% The MI5 daily administers Bond antidote a, unless he is on holiday h.
% Suppose now that, that day, Bond was actually on a holiday with Vesper.

% @nl("Bond is poisoned if he drinks the drug and does not receive the antidote")
p :- d, not a.
% @nl("Bond might be holiday or working")
{h;w}.
% @nl("Bond cannot be both on holiday and working")
:- h, w.
% @nl("Bond has to be either on holiday or working")
:- not h, not w.

% @nl("Bond receives the antidote if he is working")
a :- w.

% @nl("Bond receives the antidote if he is smart")
% a :- s.

% d:- &tag_rule{abducible(rm)}.

%==== Instance

%*
a
....
Bond receives the antidote

%*!
d
..
Bond has drunk the drug
*%
% @nl("Bond has drunk the drug") : d

%*!
d(X)
..
Bond has drunk the drug

Args:
    X (fun) : drug
*%
% @nl("Bond has drunk the drug", X) : d(X)


% @nl("Bond has received the antidote")
% #defined a/0.


% :- a, not &tag_atom{nl("Bond has received the antidote.",())}.


% @nl("Bond has drunk the drug")
#defined d/0.
% @nl("Bond has been poisoned")
#defined p/0.
% @nl("Bond is on holiday")
#defined h/0.
% @nl("Bond is working")
#defined w/0.
% @nl("Bond is smart")
#defined s/0.
