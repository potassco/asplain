
{sit(P);stand(P)}:-person(P), &tag_rule{nl("{} can sit or stand",(P,))}.
:- person(P), not sit(P), not stand(P), &tag_rule{nl("{} has to either sit or stand",(P,))}.
:- sit(P), stand(P), &tag_rule{nl("{} can't sit and stand",(P,))}.

% Alternatively, we could use a choice with bounds
% 1{sit(P);stand(P)}1:-person(P).

over_age(P):- age(P,E), E>60, &tag_rule{nl("{} is overage since they are older than 60",(P,))}.
child(P):- age(P,E), E<10, &tag_rule{nl("{} is a child since they are younger than 10",(P,))}.
:- stand(P), over_age(P), &tag_rule{nl("{} can't stand since they are overage",(P,))}.
:- stand(P), child(P), &tag_rule{nl("{} can't stand since they are a child",(P,))}.


% over_age(P):- not child(P), person(P).


% Maybe we want to add externals for all abducible atoms to already have them in the graph.
% But would not be so nice for things like this:
% #external age(P,1..80):person(P).

#external over_age(P):person(P).

#external child(P):person(P).


% Labels for atoms
:- person(P), not &tag_atom{nl("{} is a person",(P,))}.
:- age(P,E), not &tag_atom{nl("{} is {} years old",(P,E))}.
:- child(P), not &tag_atom{nl("{} is a child",(P,))}.
:- over_age(P), not &tag_atom{nl("{} is overage",(P,))}.
:- sit(P), not &tag_atom{nl("{} is sitting",(P,))}.
:- stand(P), not &tag_atom{nl("{} is standing",(P,))}.



% ## Input
person(anna):-&tag_rule{nl("Input",())}, &tag_rule{abducible(rm)}.
age(anna,70):-&tag_rule{nl("Input",())}, &tag_rule{abducible(rm)}.
person(eva):-&tag_rule{nl("Input",())}, &tag_rule{abducible(rm)}.
age(eva,8):-&tag_rule{nl("Input",())}, &tag_rule{abducible(rm)}.

age(eva,20):-&tag_rule{disabled}, &tag_rule{abducible(add)}.
% child(anna):-&tag_rule{nl("Maybe",())},&tag_rule{disable}.


% Age as an abducible might lead to an interesting difference function
