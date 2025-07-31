%% *******************
% Selects a single reason for each true atom
%% *******************
1{  reason((rule(disjunction(H),B),atom(A))):edge((rule(disjunction(H),B),atom(A))), hold(rule(disjunction(H),B));
    reason((rule(choice(H),B),atom(A))):edge((rule(choice(H),B),atom(A))), hold(rule(choice(H),B))}1      :- hold(atom(A)).

% A disjunction can only be the reason for a single atom.
:-  reason((rule(disjunction(H),B),atom(A))), reason((rule(disjunction(H),B),atom(A'))), A>A'.

%% *******************
% ## Cycle free masks
%% *******************

% A cycle can not be present since it would imply a self-founded loop.
% Cycle free reasons are stable models since they must have external support.
path_type(positive,1).
path_type(negative,0).

path(P,A1,A2):-
    % there is a X edge from A1 to R1
    edge((atom(A1),rule(H,B))),
    edge_attr((atom(A1),rule(H,B)), type, T),
    path_type(T,P),
    % R1 is the head of the reason for A2
    reason((rule(H,B),atom(A2))).

% Transitivity
path((P1+P2)\2, A1, A3):-path(P1,A1,A2), path(P2,A2, A3).

% No cycles
:- path(_,A,A).
