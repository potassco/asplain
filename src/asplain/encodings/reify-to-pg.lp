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

% Error occurs when a sum is encountered in the input (unsupported)

error("Sum not supported") :- rule(H,sum(B)).

% Gather all rules and atoms

label(rule(H,B), @label(rule(H,B))) :- rule(H,B).
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
program(N, ref):-node(N,_), not optional(add, N).
#show program/2.

% Tags into reference graph
asplain_tag(R,T):-tag(rule(H,B),T), label(rule(H,B),R).
asplain_tag(A,T):-tag(atom(E),T), symbol_literal(A,E).

#show tag(N,T): asplain_tag(N,T).

% Optional to remove
optional(remove, R):-asplain_tag(R, removable).
% For now dynamic tags are not added here
% optional(remove, rule(disjunction(H),B)):-
%     tag(G, rule(disjunction(H),B),fact), %is a fact
%     removable_if_fact(A), %flagged as removable if A
%     atom_tuple(H,E), %the head atom is A
%     symbol_literal(A,E).

% Optional to add also includes the edges that would be added
optional(add, R):-asplain_tag(R, addable).

#show optional/2.

#include "utils-tags.lp".
