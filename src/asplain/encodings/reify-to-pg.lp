

error("Sum not supported") :- rule(H,sum(B)).

node(reference, rule(H,B)):-rule(H,B).
node(reference, atom(A)):-symbol_literal(A,L).

edge(reference, positive, (atom(A), rule(H,normal(B)))):-
    rule(H,normal(B)),
    literal_tuple(B,E),
    E>0, symbol_literal(A,E),
    node(reference,atom(A)),
    node(reference,rule(H,normal(B))).

edge(reference, negative, (atom(A), rule(H,normal(B)))):-
    rule(H,normal(B)),
    literal_tuple(B,E),
    E<0, symbol_literal(A,-E),
    node(reference,atom(A)),
    node(reference,rule(H,normal(B))).

edge(reference, positive, (rule(disjunction(H),B),atom(A))):-rule(disjunction(H),B),
    atom_tuple(H,E), symbol_literal(A,E).

edge(reference, positive, (rule(choice(H),B),atom(A))):-rule(choice(H),B),
    atom_tuple(H,E), symbol_literal(A,E).


#show node/2.
#show edge/3.


% Extra tags
tag(rule(disjunction(H),B), constraint):- rule(disjunction(H),B), not atom_tuple(H,_).
tag(rule(disjunction(H),normal(B)), fact):- rule(disjunction(H),normal(B)),
    #count{E:atom_tuple(H,E)}=1,
    not literal_tuple(B,_).

% Assumptions removable
tag(R, abducible(remove)):-tag(R, assume(_)).
tag(R, label("User assumed {} as {}",(A,F))):-tag(R, assume(F)), edge(G, _, (atom(A),R)).

% Labels without vars
tag(R, label(L,())):-tag(R, label(L)).

% Removable if fact
tag(G, R, abducible(remove)):- tag(G, R,fact),  edge(G, _, (R, atom(A))), removable_if_fact(A).
tag(G, R, abducible(add)):- tag(G, R,program(addable)).
tag(G, R, disabled):- tag(G, R,program(addable)).

% Tags into reference mode
tag(reference,rule(H,B),T):-tag(rule(H,B),T).
tag(reference,atom(A),T):-tag(atom(E),T), symbol_literal(A,E).

#show tag/3.
