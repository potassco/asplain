


% p(1..4).
% {c}.

% {r(X):p(X);#true} :- c.



% p(1):-&tag_rule{input}.
% p(2):-&tag_rule{input}.
% p(3):-&tag_rule{input}.
% c:-&tag_rule{input}.

% % 1{r(X):p(X)}1 :- c, &tag_rule{nl("At most one",())}.
% % 1 {r(X):p(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% % 1 {r(X):p(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% {r(X)} :- p(X), c, &tag_rule{nl("Choose",())}.
% :-   #sum{1,X:r(X)} !=1, c, &tag_rule{nl("Can't be other than one",())}.
% % 1 {r(X):p(X)} 1 :- c, &tag_rule{nl("Choose",())}.
% % {r(X):p(X),p(X+1)} 1 :- c, &tag_rule{nl("Choose",())}.

% % {r(X):p(X)} 1 :- c, &tag_rule{nl("Choose",())}.

% % :-   #sum{1,X:r(X),p(X)} != 1, c, &tag_rule{nl("Can't be one",())}.
% % :- #sum{1,r(X):p(X)}!=1, c, &tag_rule{nl("At most one",())}.
% % {r(X)} :- c, p(X).


b:-&tag_rule{rule(1)}.
c:-&tag_rule{rule(2)}.
a:-b, &tag_rule{rule(3)}.
a:-c, &tag_rule{rule(4)}.

% b.
% c.
% a:-b.
% a:-c.

% aL
