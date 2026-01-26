% Extra tags
% Note that it uses the original tag/2 and the the other file is the one that creates the asplain_tag/2
tag(rule(disjunction(H),B), constraint):- rule(disjunction(H),B), not atom_tuple(H,_).
tag(rule(disjunction(H),normal(B)), fact):- rule(disjunction(H),normal(B)),
    #count{E:atom_tuple(H,E)}=1,
    not literal_tuple(B,_).

% Assumptions removable
tag(R, label("Assumed {} as {}",(A,F))):-tag(R, assume(F)), edge(G, _, (atom(A),R)).
% Maybe this next rule should be optional
abducible(remove,R):-tag(reference, R, assume(_)).

% Labels without vars
tag(R, label(L,())):-tag(R, label(L)).

show(A,L):-show_atom(A,L).
show(A,L):-show_term(A,L).
tag(atom(E), shown):- show(A,L), symbol_literal(A,E). %Show all explicit
tag(atom(E), shown):-symbol_literal(A,E), not show, not show_atom(_,_). %Show all unless hide or show signature
