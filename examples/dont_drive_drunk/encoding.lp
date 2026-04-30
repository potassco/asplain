% @label("{} is a person",(P,)) :: person(P)
% @label("{} is driving",(P,)) :: drive(P)
% @label("{} is drinking alcohol",(P,)) :: alcohol(P)
% @label("{} is resisting the authorities",(P,)) :: resist(P)
% @label("{} is punished",(P,)) :: punish(P)
% @label("{} is sentenced to prison",(P,)) :: sentence(P, prison)
% @label("{} is innocent",(P,)) :: sentence(P, innocent)

% @label("{} is punished since they drove drunk",(P,))
punish(P) :- drive(P), alcohol(P),  person(P).
% @label("{} is punished since they resisted the authorities ",(P,))
punish(P) :- resist(P), person(P).

% @label("{} is innocent since they were not punished",(P,))
sentence(P, prison) :- punish(P).
% @label("{} is innocent since they were not punished",(P,))
sentence(P, innocent) :- person(P), not punish(P).


% ----- Instance
person(gabriel).
person(clare).
% @removable
drive(gabriel).
% @removable
alcohol(gabriel).
% @removable
drive(clare).



#program asplain.
% @label("{} is resisting the authorities",(P,))
% @addable
resist(P):-person(P).
