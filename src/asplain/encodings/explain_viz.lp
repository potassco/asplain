#include "reify_defined.lp".

#const true_color = @color(green,50).

%============== RULES
node(rule(H,B)):-rule(H,B), not aux_rule(rule(H, B)).
attr(node,rule(H,B),style,filled):-rule(H,B), not aux_rule(rule(H, B)).
attr(node,rule(H,B),shape,box):-rule(H,B), not aux_rule(rule(H, B)).
attr(node,rule(H,B),fillcolor,true_color):-rule(H,B), body(B).
% attr(node,rule(choice(H),B),shape,box):-rule(choice(H),B), not aux_rule(choice(H), B).

% Aux rules are the choices for _rule
aux_rule(rule(choice(H),normal(B))):- rule(choice(H),normal(B)),
    aux_atom(S):atom_tuple(H,E), E>0, atom(E,P), atom_value(E,P,S).

attr(node,rule(H,B),label,"<<i>{{input}}</i><br/> <b>BODY {{value}}</b> <br/><i>{{output}}</i>>"):-rule(H,B),
    not aux_rule(rule(H,B)).

attr(node,rule(H,normal(B)),(label,value),X):-rule(H,normal(B)),
    literal_tuple(B,E), E>0, atom(E,P), atom_value(E,P,_rule(X)).
attr(node,rule(H,B),(label,value),"aux"):-rule(H,B),
    not attr(node,rule(H,B),(label,value),X):output(_rule(X), _).

attr(node,rule(choice(H),B),(label,output),"choice"):-rule(choice(H),B), not aux_rule(rule(choice(H),B)).
attr(node,rule(disjunction(H),B),(label,output),"disjuction"):-rule(disjunction(H),B), not aux_rule(rule(disjunction(H),B)).

attr(node,rule(H,normal(B)),(label,input),"normal"):-rule(H,normal(B)), not aux_rule(rule(H,normal(B))).
attr(node,rule(H,sum(B,G)),(label,input),@concat("sum at least",G)):-rule(H,sum(B,G)), not aux_rule(rule(H,sum(B,G))).


%============== ATOMS
atom(E, atom_tuple(A,E)):- atom_tuple(A,E), E>0.
% atom(-E, atom_tuple(A,E)):- atom_tuple(A,E), E<0.
atom(E, external(E,V)):- external(E,V).
% atom(E, theory_atom(E,S,ET)):- theory_atom(E,S,ET).%Theory atom without guard
% atom(E, theory_atom(E,S,ET,ID_G,ID_S)):- theory_atom(E,S,ET,ID_G,ID_S).%Theory atom with guard


aux_atom(_rule(X)):- output(_rule(X), _).

node(S):-atom(E,P),atom_value(E, P, S), not aux_atom(S).
attr(node,(S),style,filled):- atom(E,P), atom_value(E, P, S), not aux_atom(S).
attr(node,(S),fillcolor,true_color):- atom(E,P), atom_value(E, P, S), not aux_atom(S), hold(E).

atom_value(E, P, S):- atom(E, P), literal_tuple(L,E), output(S,L).
atom_value(E, P, @concat("aux_",E)):- atom(E, P), not atom_value(E,P, S): output(S, _).


edge((S,rule(H,normal(B)))):-
    rule(H,normal(B)), literal_tuple(B,E), E>0, atom(E,P), atom_value(E,P,S), node(S).
edge((S,rule(H,normal(B)))):-
    rule(H,normal(B)), literal_tuple(B,E), E<0, atom(-E,P), atom_value(-E,P,S), node(S).
attr(edge,(S,rule(H,normal(B))),style,dotted):-
    rule(H,normal(B)), literal_tuple(B,E), E<0, atom(-E,P), atom_value(-E,P,S), node(S).


edge((S,rule(H,sum(B,G)))):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E>0, atom(E,P), atom_value(E,P,S), node(S).
edge((S,rule(H,sum(B,G)))):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E<0, atom(-E,P), atom_value(-E,P,S), node(S).
attr(edge,(S,rule(H,sum(B,G))),style,dotted):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E<0, atom(-E,P), atom_value(-E,P,S), node(S).
attr(edge,(S,rule(H,sum(B,G))),label,W):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E>0, atom(E,P), atom_value(E,P,S), node(S).
attr(edge,(S,rule(H,sum(B,G))),label,W):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E<0, atom(-E,P), atom_value(-E,P,S), node(S).
% edge((literal_tuple(I),P)):-literal_tuple(I,E), E>0, atom(E,P).

attr(edge,(rule(H,normal(B)),literal_tuple(B)),label,"body"):-rule(H,normal(B)).


% HEAD
edge((rule(disjunction(H),B),S)):-rule(disjunction(H),B),
    atom_tuple(H,E), atom(E,P), atom_value(E,P,S).

edge((rule(choice(H),B),S)):-rule(choice(H),B),
    not aux_rule(rule(choice(H), B)),
    atom_tuple(H,E), atom(E,P), atom_value(E,P,S).
