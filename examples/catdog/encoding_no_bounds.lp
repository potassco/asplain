%*

Sits people so that dog people dont sit in the same table as dog people

#person(A,P)
    `A` is a person that likes pet `P`
    - A : Name of the person
    - P : the pet either `dog` or `cat`

#seat((T,C))
    There is a seat identified by table `T` and chair `C`
    - T : Table number
    - C : Chair number

#assign(P,S)
    Assigns a person to a seat
    - P : Name of the person
    - S : Seat where S= (T,C) where T is the table number and C is the chair number

*%

%=== Instance
person("Susana",cat):- &tag_rule{input}.
person("Alexander",cat):- &tag_rule{input}.
person("Torsten",dog):- &tag_rule{input}.
seat((1,1..2)):- &tag_rule{input}.
seat((2,1..2)):- &tag_rule{input}.

:- person(P,A), not &tag_atom{nl("{} likes {}s",(P,A))}.
:- seat((T,C)), not &tag_atom{nl("There is a seat at table {} and chair {}",(T,C))}.
:- assign(P,(T,C)), not &tag_atom{nl("{} is assigned to table {} chair {}",(P,T,C))}.

% ---- encoding
% 0{assign(P,S):seat(S)}#sup:- person(P,A).
% 1{assign(P,S):seat(S)}1:- person(P,A).
{assign(P,(T,C))}:- person(P,A), seat((T,C)), &tag_rule{nl("{} might be assigned to table {} seat {}",(P,T,C))}.
% {assign(P,S)}:- person(P,A),seat(S).

% :- assign(P,S), assign(P,S'), S'>S.  % no seats assigned to the same person
% :- person(P,A), not assign(P,S): seat(S).  % every person must be assigned to a seat

:- #sum{1,S:assign(P,S)}!=1, person(P,A), &tag_rule{nl("{} must be assigned to exactly one seat",P)}.  % every person must be assigned to a seat


% :- assign(P,S), assign(P,S'), S'>S.  % no seats assigned to the same person
:- assign(P,S), assign(P',S), P'>P, &tag_rule{nl("{} and {} can't share seat",(P,P'))}.  % no two people in the same seat
:- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog), &tag_rule{nl("{} and {} don't like the same animal<br/> so can't seat in the same table {}",(P,P',T))}. % no cat and dog people in the same seat

%% Interaction 1:
% query:
% why torsten and susana cannot be in the same table?
% q :- assign("Susana",(T,_)), assign("Torsten",(T,_)), table(T).
% :- not q.b

%% Interaction 2:
% promted:
% assign("Torsten", (1,1)) not assign("Susana", (1,2))
% query:
% why Susana is not with Torsten in table 1?
% q :- assign("Susana", (1,_)).
% :- not q.

% ---- assumed

% query
% assign("Susana",(1,2))
