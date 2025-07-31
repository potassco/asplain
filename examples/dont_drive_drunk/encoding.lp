
% ----- Encoding
% The tags are manually added but an llm could do it automatically. Specially with a program that has comments
punish(P) :- drive(P), alcohol(P),  person(P), &tag_rule{nl("{} is punished since they drove drunk",(P,))}.
punish(P) :- resist(P), person(P), &tag_rule{nl("{} is punished since they resisted the authorities ",(P,))}.

sentence(P, prison) :- punish(P), &tag_rule{nl("{} is sentenced to prison since they where punished",(P,))}.
sentence(P, innocent) :- person(P), not punish(P), &tag_rule{nl("{} is innocent since they where not punished",(P,))}.



% ----- Instance
% This tags can be automatic for all input facts (which usually come from the instance, then the preference can say which input is abducible)
% Another relevant tag for input things is if they are static input, for instance, person(P) is static and can't be aduced and perhaps we even want to hide this in the graph.
% While alcohol(P) is dynamic and can be adduced and it is relevant for explanation. But this might be just preferences of the graph pruning
person(gabriel):- &tag_rule{input}.
person(clare):-&tag_rule{input}.
drive(gabriel):-&tag_rule{input}.
alcohol(gabriel):-&tag_rule{input}.
drive(clare):-&tag_rule{input}.
% Just like we tag this we could tag integrity constraints and have a preference that allows abducing them to find the errors



% Meaning of atoms
% This would be what the user needs to input, perhaps in another format that is simpler
% This might even come from the documentation of the program since document the atoms is the basic expected documentation
% The reason why it is in an integrity constraint was so that if all tag_atom and tag_rule are true they become irrelevant
% This would have been done by a propagator but at the moment it is achieved by simply ignoring theory atoms in the PG
:- person(P), not &tag_atom{nl("{} is a person",(P,))}.
:- drive(P), not &tag_atom{nl("{} is driving",(P,))}.
:- alcohol(P), not &tag_atom{nl("{} is drinking alcohol",(P,))}.
:- resist(P), not &tag_atom{nl("{} is resisting the authorities",(P,))}.
:- punish(P), not &tag_atom{nl("{} is punished",(P,))}.
:- sentence(P, prison), not &tag_atom{nl("{} is sentenced to prison",(P,))}.
:- sentence(P, innocent), not &tag_atom{nl("{} is innocent",(P,))}.



% ----- Safety for any instance if we want to allow some rules to be added if not present
% This would be for any type of rule but can be used for unknown input.
% Similar to #defined alcohol(clare).

% alcohol(clare):-&tag_rule{disabled},&tag_rule{nl("Optional Input")}.
% alcohol(gabriel):-&tag_rule{disabled},&tag_rule{nl("Optional Input")}.

alcohol(P):-person(P), &tag_rule{disabled}.
