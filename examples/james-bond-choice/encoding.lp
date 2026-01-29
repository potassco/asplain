% @label("Bond takes the antidote") :: a
% @label("Bond is poisoned") :: p
% @label("Bond is careful") :: c
% @label("Bond has contact with toxin") :: t


% @label("Bond might drink martini")
{d}.

% @label("Can't be poisoned if antidote was taken")
:- p, a.

% @label("Bond is poisoned due to toxin")
p :- t.
% @label("Bond is poisoned if drinks and not careful")
p :- d, not c.

% @removable
a.

% @removable
c.

#program addable.
t.
