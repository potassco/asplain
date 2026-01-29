% @label("Takes the antidote") :: a
% @label("Is poisoned") :: p
% @label("Is careful") :: c
% @label("Contact with toxin") :: t


% @label("Might drink")
{d}.

% @label("Can't be poisoned if antidote taken")
:- p, a.

% @label("Is poisoned due to toxin")
p :- t.
% @label("Is poisoned if drinks and not careful")
p :- d, not c.

% @removable
a.

% @removable
c.

#program addable.
t.
