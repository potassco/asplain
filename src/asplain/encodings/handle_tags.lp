% Transforms a reified program in to a program graph
%
% !!! warning Assumes one body for each rule, which is achieved by tagging each rule with a unique ID
% !!! warning Assumes all atoms are set as external?
% --------------------------------------------------------
rule_tag(F,ID_A):-theory_atom(ID_A,ID_O,ID_E),
            theory_string(ID_O,"tag_rule"),
            theory_element_tuple(ID_E,ID_EE),

            theory_element(ID_EE,ID_T,_),
            theory_tuple(ID_T,0,ID),
            theory_symbol(ID,F).

atom_tag(F,ID_A):-theory_atom(ID_A,ID_O,ID_E),
            theory_string(ID_O,"tag_atom"),
            theory_element_tuple(ID_E,ID_EE),

            theory_element(ID_EE,ID_T,_),
            theory_tuple(ID_T,0,ID),
            theory_symbol(ID,F).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ## Auxiliaries
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% special atoms and rules to handle the `_rule` tags which come from `{_rule(X)}`.
%*
#aux_atom(A)
Atom `A` is auxiliary
*%
% aux_atom(_rule(X)):- output(_rule(X), _).
%*
#aux_rule(R)
Rule `R` is auxiliary

#parameters
- R: is of form rule(choice(H),normal(B))
*%
% aux_rule(rule(disjunction(H),normal(B))):-
%     rule(disjunction(H),normal(B)),
%     literal_tuple(B,L), rule_tag(F,L).

aux_rule(rule(H,normal(B))):-
    rule(H,normal(B)),
    literal_tuple(B,-L), atom_tag(F,L).

% Rules that are disabled are removed.
aux_rule(rule(H,normal(B))):-
    rule(H,normal(B)),
    literal_tuple(B,L), rule_tag(disable,L).


node_tag(rule(H,normal(B)),F):-
    rule(H,normal(B)),
    literal_tuple(B,L), rule_tag(F,L).


node_tag(atom(A),F):-
    rule(disjunction(H),normal(B)),
    literal_tuple(B,-L), atom_tag(F,L),
    literal_tuple(B, E), E!=L,
    atom_value(E, A).


% #show aux_rule/1.
#show node_tag/2.



% ---------- extra inferred tags

node_tag(rule(H,B),nl("User assumed {}",(F,))):-
    node_tag(rule(H,B),assume(F)).

node_tag(rule(H,B),abducible(rm)):-
    node_tag(rule(H,B),assume(_)).

node_tag(rule(H,B),nl("Input",())):-
    node_tag(rule(H,B),input).
