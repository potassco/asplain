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
person("Susana",cat). person("Alexander",cat). person("Torsten",dog).
seat((1,1..2)). seat((2,1..2)).

% ---- encoding
1{assign(P,S):seat(S)}1:- person(P,A).


:- assign(P,S), assign(P',S), P'>P.
:- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog).

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

assign("Torsten", (1,1)).
% query
% assign("Susana",(1,2))
