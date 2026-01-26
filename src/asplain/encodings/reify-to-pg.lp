#script (python)
from clingo import Number
ids = {}
def rule_id(rule):
    if str(rule) in ids:
        n= ids[str(rule)]
    else:
        id = len(ids) + 1
        ids[str(rule)] = id
        n = id
    return Number(n)
#end.


error("Sum not supported") :- rule(H,sum(B)).

% Create PG_Rs,

% Gather all rules and atoms
rule_id(rule(H,B), @rule_id(rule(H,B))) :- rule(H,B).
node(R):-rule(H,B), rule_id(rule(H,B),R).
node(A):-symbol_literal(A,L).
node_type(A,atom):-symbol_literal(A,L).
node_type(R,rule(disjunction)):-rule_id(rule(disjunction(H),B), R).
node_type(R,rule(choice)):-rule_id(rule(choice(H),B), R).

% Gather all edges
edge(E):-edge_type(E,_).

edge_type((A, R),1):-
    rule_id(rule(H, normal(B)), R),
    literal_tuple(B,E), E>0, symbol_literal(A,E).

edge_type((A, R),0):-
    rule_id(rule(H, normal(B)), R),
    literal_tuple(B,E), E<0, symbol_literal(A,-E).

edge_type((R, A),1):-
    rule_id(rule(disjunction(H), B), R),
    atom_tuple(H,E), symbol_literal(A,E).

edge_type((R, A),1):-
    rule_id(rule(choice(H), B), R),
    atom_tuple(H,E), symbol_literal(A,E).

#show node/1.
#show node_type/2.
#show edge/1.
#show edge_type/2.

% Program membership for reference
p_member(N, ref):-node(N), not abducible(add, N).
% p_member((N1,N2), ref):-edge((N1,N2)), p_member(N1, ref), p_member(N2, ref).
#show p_member/2.

% Define what is reference
% node(@rule_id(rule(H,B))):-rule(H,B), not abducible(add, rule(H,B)).

% ------- Tags ------
% Tags into reference graph
asplain_tag(R,T):-tag(rule(H,B),T), rule_id(rule(H,B),R).
asplain_tag(A,T):-tag(atom(E),T), symbol_literal(A,E).

#show tag(N,T): asplain_tag(N,T).


% #show tag(G, E, T):tag(G, E, T), edge(G,_,E).
% #show tag(G, N, T):tag(G, N, T), node(G,N).

% ----- Abducibles -----

% Abducible to remove
abducible(remove, R):-asplain_tag(R, removable).
% For now dynamic tags are not added here
% abducible(remove, rule(disjunction(H),B)):-
%     tag(G, rule(disjunction(H),B),fact), %is a fact
%     removable_if_fact(A), %flagged as removable if A
%     atom_tuple(H,E), %the head atom is A
%     symbol_literal(A,E).

% Abducible to add also includes the edges that would be added
abducible(add, R):- asplain_tag(R, (program(addable);disabled)).
% I think edges we don't need to explicitly add, if we add a rule, it comes with all its edges
% abducible(add, edge((R,A)), T):- abducible(add, R), edge((R,A)), edge_type((R,A),T).
% abducible(add, edge((A,R)), T):- abducible(add, R), edge((A,R)), edge_type((A,R),T).

#show abducible/2.

#include "utils-tags.lp".
