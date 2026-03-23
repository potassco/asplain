%*
Assigns people seats so that dog people dont sit on the same table as cat people
*%

% @label("Person {} likes the pet {}",(P,A,)) :: person(P,A)
% @label("There is a seat with chair {} on table {}",(C,T,)) :: seat((T,C))
% @label("Person {} is a assigned seat {}",(P,S,)) :: assign(P,S)

% @label("Person is assigned a seat")
{assign(P,S):seat(S)}:- person(P,A).

% @label("No two people can be assigned the same seat")
:- assign(P,S), assign(P',S), P'>P.
% @label("If a person is a ssigned a seat, they're sitting")
sitting(P) :- person(P,A), assign(P,S).
% @label("Every person has to be sitting")
:- person(P,A), not sitting(P).
% @label("No cat and dog people in the same seat")
:- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog).
