
{sit(P);stand(P)}:-person(P).

:- sit(P), stand(P'), P=P'.
:- stand(P), age(P,E), E>90.

% Input facts
% sit(anna).
person(anna).
age(anna,94).
