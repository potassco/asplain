% @label("Bond takes the antidote") :: a
% @label("Bond is poisoned") :: p
% @label("Bond drinks") :: d
% @label("Bond is careful") :: c
% @label("Bond has contact with toxin") :: t


% @label("Bond might drink martini")
{d}.

% @label("Can't be poisoned he was careful")
% @removable
:- p, c.

% @label("Bond is poisoned due to contact with toxin")
p :- t.
% @label("Bond is poisoned if drinks and didnt take the antidote")
p :- d, not a.

% @removable
a.

% @removable
c.

% @removable
t.
