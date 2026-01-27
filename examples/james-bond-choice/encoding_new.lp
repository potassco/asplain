% @label("Bond has drunk the drug") :: d
% @label("Bond has received the antidote") :: a

% @label("James might drink the drug")
{d}.
% @label("Bond is poisoned if he drinks the drug and does not receive the antidote")
p :- d, not a.

% @removable
a.

% @removable
% @label("Bond decided not to drink")
:- not d.

#program addable.
% @label("Bond is directly poisoned")
p.
