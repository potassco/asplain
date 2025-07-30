


% p(1..4).
% {c}.

% {r(X):p(X);#true} :- c.



p(1):-&tag_rule{input}.
p(2):-&tag_rule{input}.
p(3):-&tag_rule{input}.
{c}.
{r(X)} :- c, p(X).
