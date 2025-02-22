
1{sit(P);stand(P)}1:-person(P).

:- stand(P), age(P,E), E>90.

% Input facts
% sit(anna).
person(anna).
age(anna,95).
