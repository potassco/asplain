% Transforms a reified program in to a program graph
%
% !!! warning Assumes one body for each rule, which is achieved by tagging each rule with a unique ID
% !!! warning Assumes all atoms are set as external?
% --------------------------------------------------------


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ## Auxiliaries
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% special atoms and rules to handle the `_rule` tags which come from `{_rule(X)}`.
%*
#aux_atom(A)
Atom `A` is auxiliary
*%
aux_atom(_rule(X)):- output(_rule(X), _).
%*
#aux_rule(R)
Rule `R` is auxiliary

#parameters
- R: is of form rule(choice(H),normal(B))
*%
aux_rule(rule(choice(H),normal(B))):- rule(choice(H),normal(B)),
    aux_atom(A):atom_tuple(H,E), atom(E,P), atom_value(E,A).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ## Nodes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%*
#node(N)
Node `N` is a node in the graph

#parameters
- N: is of form `rule(H,B)` or `atom(A)`, where `A` is an atom
*%

% ### Rule nodes
% All rules in the reification except the auxiliary ones
node(rule(H,B)):-rule(H,B), not aux_rule(rule(H, B)).

% ### Atom nodes

% Gather all atoms in the program, considering only the positive ones
% We also include the externals to account for the atoms removed in the grounding
%*
#atom(E, P)
An atom identified by number `E` is in the program coming from `P`
*%
atom(E, atom_tuple(A,E)):- atom_tuple(A,E), E>0.
atom(E, external(E,V)):- external(E,V).

%*
#atom_value(E, A)
An atom identified by `E` is in the program and has value `A`.
Any atom that can not be mapped into an auxiliary has a as name aux(E)
!!! example
    ```atom_value(10, person(james))```
*%
atom_value(E, A):- atom(E, _), literal_tuple(L,E), output(A,L).
atom_value(E, aux(E)):- atom(E, _), not atom_value(E, A): output(A, _).

node(atom(A)):-atom(E,_), atom_value(E, A), not aux_atom(A).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ## Edges
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%*
#edge((N1,N2))
Edge between nodes `N1` and `N2`
*%

% ### Body atoms to rule

% #### Normal edges

% Edges for positive literals
edge((atom(A),rule(H,normal(B)))):-
    rule(H,normal(B)), literal_tuple(B,E), E>0, atom(E,_), atom_value(E,A), node(atom(A)).
edge_attr((atom(A),rule(H,normal(B))), type, positive):-
    rule(H,normal(B)), literal_tuple(B,E), E>0, atom(E,_), atom_value(E,A), node(atom(A)).
% Edges for negative literals
edge((atom(A),rule(H,normal(B)))):-
    rule(H,normal(B)), literal_tuple(B,E), E<0, atom(-E,_), atom_value(-E,A), node(atom(A)).
edge_attr((atom(A),rule(H,normal(B))), type, negative):-
    rule(H,normal(B)), literal_tuple(B,E), E<0, atom(-E,_), atom_value(-E,A), node(atom(A)).

% #### Sum edges

% Edges for positive literals
edge((atom(A),rule(H,sum(B,G)))):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,_), E>0, atom(E,_), atom_value(E,A), node(atom(A)).
edge_attr((atom(A),rule(H,sum(B,G))), type, positive):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,_), E>0, atom(E,_), atom_value(E,A), node(atom(A)).
edge_attr((atom(A),rule(H,sum(B,G))), weight, W):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E>0, atom(E,_), atom_value(E,A), node(atom(A)).
% Edges for negative literals
edge((atom(A),rule(H,sum(B,G)))):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,_), E<0, atom(-E,_), atom_value(-E,A), node(atom(A)).
edge_attr((atom(A),rule(H,sum(B,G))), type, negative):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,_), E<0, atom(-E,_), atom_value(-E,A), node(atom(A)).
edge_attr((atom(A),rule(H,sum(B,G))), weight, W):-
    rule(H,sum(B,G)), weighted_literal_tuple(B,E,W), E<0, atom(-E,_), atom_value(-E,A), node(atom(A)).


% ### Rule body to head atoms
edge((rule(disjunction(H),B),atom(A))):-rule(disjunction(H),B),
    atom_tuple(H,E), atom(E,P), atom_value(E,A).

edge((rule(choice(H),B),atom(A))):-rule(choice(H),B),
    not aux_rule(rule(choice(H), B)),
    atom_tuple(H,E), atom(E,P), atom_value(E,A).
