
% {sit(P);stand(P)}:-person(P).
% :- person(P), not sit(P), not stand(P).
% :- sit(P), stand(P).

% Alternatively, we could use a choice with bounds
% 1{sit(P);stand(P)}1:-person(P).

over_age(P):- age(P,E), E>60.
child(P):- age(P,E), E<10.
:- stand(P), over_age(P).
:- stand(P), child(P).


% over_age(P):- not child(P), person(P).


% Maybe we want to add externals for all abducible atoms to already have them in the graph.
% But would not be so nice for things like this:
% #external age(P,1..80):person(P).

#external over_age(P):person(P).
#external child(P):person(P).


% ## Input
person(anna).
age(anna,70).
person(eva).
age(eva,8).

% Age as an abducible might lead to an interesting difference function
