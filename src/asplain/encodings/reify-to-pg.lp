#script (python)
from clingo import Number
ids = {}
def label(rule):
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

% label(rule(H,B), @label(rule(H,B))) :- rule(H,B). % <-------- Correct line
label(rule(H,B), ID) :- tag(rule(H,B),rule_id(ID)). % <--------  HACK just for the paper
node(A,atom) :- symbol_literal(A,L).
node(R,rule(disjunction)) :- label(rule(disjunction(H),B), R).
node(R,rule(choice)) :- label(rule(choice(H),B), R).

% Gather all edges

edge((A, R),1):-
    label(rule(H, normal(B)), R),
    literal_tuple(B,E), E>0, symbol_literal(A,E).

edge((A, R),0):-
    label(rule(H, normal(B)), R),
    literal_tuple(B,E), E<0, symbol_literal(A,-E).

edge((R, A),1):-
    label(rule(disjunction(H), B), R),
    atom_tuple(H,E), symbol_literal(A,E).

edge((R, A),1):-
    label(rule(choice(H), B), R),
    atom_tuple(H,E), symbol_literal(A,E).

#show node/2.
#show edge/2.

% Program membership for reference
program(N, ref):-node(N,_), not abducible(add, N).
#show program/2.

% ------- Tags ------
% Tags into reference graph
asplain_tag(R,T):-tag(rule(H,B),T), label(rule(H,B),R).
asplain_tag(A,T):-tag(atom(E),T), symbol_literal(A,E).

#show tag(N,T): asplain_tag(N,T).


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
abducible(add, R):-asplain_tag(R, addable).

#show abducible/2.

#include "utils-tags.lp".
