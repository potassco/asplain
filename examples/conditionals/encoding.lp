


% o(1..4).
% {c}.

% {s(X):o(X);#true} :- c.



o(1).
o(2).
o(3).
c.
b.

% 1{s(X):o(X)}1 :- c, &tag_rule{nl("At most one",())}.
% % 1 {s(X):o(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% % 1 {s(X):o(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% {s(X)} :- o(X), c, &tag_rule{nl("Choose",())}.
% :-   #sum{1,X:s(X)} !=1, c, &tag_rule{nl("Can't be other than one",())}.
% % 1 {s(X):o(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% % {s(X):o(X),o(X+1)} 1 :- c, &tag_rule{nl("Choose",())}.

{s(X):o(X)} :- c, &tag_rule{nl("Choose",())}.
% :-  not  2 #sum{1,X:s(X)} 2, c, &tag_rule{nl("Can't be one",())}.
goal:- 2 #sum{1,X:s(X)}2 , c, &tag_rule{nl("Goal if sit at least two",())}.


% 2{s(X):o(X)}2 :- c, b, &tag_rule{nl("Choose",())}.
% :-  no t  2 #sum{1,X:s(X)} 2, c, &tag_rule{nl("Can't be one",())}.

% % :- #sum{1,s(X):o(X)}!=1, c, &tag_rule{nl("At most one",())}.
% % {s(X)} :- c, o(X).


% b:-&tag_rule{rule(1)}.
% c:-&tag_rule{rule(2)}.
% a:-b, &tag_rule{rule(3)}.
% a:-c, &tag_rule{rule(4)}.

% b.
% c.
% a:-b.
% a:-c.

% aL
