

error("Sum not supported") :- rule(H,sum(B)).

node(reference, rule(H,B)):-rule(H,B), not abducible(add, rule(H,B)).
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
#show edge(G,T,(N1,N2)):edge(G,T,(N1,N2)), node(G,N1), node(G,N2).


% ------- Tags ------
% Tags into reference graph
tag(reference,rule(H,B),T):-tag(rule(H,B),T).
tag(reference,atom(A),T):-tag(atom(E),T), symbol_literal(A,E).


tag(rule(disjunction(H),B), constraint):- rule(disjunction(H),B), not atom_tuple(H,_).
tag(rule(disjunction(H),normal(B)), fact):- rule(disjunction(H),normal(B)),
    #count{E:atom_tuple(H,E)}=1,
    not literal_tuple(B,_).

% Assumptions removable
tag(R, label("User assumed {} as {}",(A,F))):-tag(R, assume(F)), edge(G, _, (atom(A),R)).

% Labels without vars
tag(R, label(L,())):-tag(R, label(L)).


#show tag(G, E, T):tag(G, E, T), edge(G,_,E).
#show tag(G, N, T):tag(G, N, T), node(G,N).

% ----- Abducibles -----

% Abducible to remove
abducible(remove,R):-tag(reference, R, assume(_)).
abducible(remove,R):-tag(reference, R, removable).
abducible(remove, rule(disjunction(H),B)):-
    tag(G, rule(disjunction(H),B),fact), %is a fact
    removable_if_fact(A), %flagged as removable if A
    atom_tuple(H,E), %the head atom is A
    symbol_literal(A,E).

% Abducible to add also includes the edges that would be added
abducible(add, R):- tag(R, (program(addable);disabled)).
abducible(add, edge(S, (R,A))):- abducible(add, R), edge(G, S, (R,A)).
abducible(add, edge(S, (A,R))):- abducible(add, R), edge(G, S, (A,R)).

#show abducible/2.
