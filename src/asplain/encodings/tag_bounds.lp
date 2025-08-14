% Generates nl tags for the parts of the program graph that talk about the bounds


node_tag(R, sumlb):-
    R = rule(disjunction(H),sum(B,W)),
    node(R),
    edge((R,atom(aux(A)))),
    edge((atom(aux(A)),R')),
    edge_attr((atom(aux(A)),R'),type,positive).

node_tag(R, sumub):-
    R = rule(disjunction(H),sum(B,W)),
    node(R),
    edge((R,atom(aux(A)))),
    edge((atom(aux(A)),R')),
    edge_attr((atom(aux(A)),R'),type,negative).


node_tag(R, nl("Lower bound calculation expected")):-node_tag(R, sumlb).
node_tag(rule(H,sum(B,W)), nl("(Not) Upper bound calculation expected")):-node_tag(rule(H,sum(B,W)), sumub).
% node_tag(rule(H,sum(B,W)), nl(@format("Upper bound calculation at most",W-1))):-node_tag(rule(H,sum(B,W)), sumub).


node_tag(N, lb_atom):-
    node_tag(R, sumlb),
    edge((R,N)).

node_tag(N, nl("LB correct")):-
    node_tag(N, lb_atom).

node_tag(N, ub_atom):-
    node_tag(R, sumub),
    edge((R,N)).

node_tag(N, nl("UB incorrect")):-
    node_tag(N, ub_atom).


node_tag(R, bounds_correct):-
    node_tag(N, lb_atom),
    node_tag(N', ub_atom),
    edge((N,R)),
    edge((N',R)).

node_tag(R, nl("Bounds correct if (Not) UB incorrect and LB correct")):-
    node_tag(R, bounds_correct).


node_tag(N, bounds_correct_atom):-
    node_tag(R, bounds_correct),
    edge((R,N)).

node_tag(N, nl("Bounds correct")):-
    node_tag(N, bounds_correct_atom).



node_tag(atom(aux(A)), conditional_ag_fired):-
    edge((atom(aux(A)),R)),
    node_tag(R, sumlb;sumub).

node_tag(atom(aux(A)), nl("Conditional for aggregation fired")):-
    node_tag(atom(aux(A)), conditional_ag_fired).

node_tag(atom(aux(A)), body_choice):-
    edge((atom(aux(A)),R)),
    R= rule(choice(H),B).

node_tag(atom(aux(A)), nl("Conditions for choice fulfilled")):-
    node_tag(atom(aux(A)), body_choice).



node_tag(R, choice_condition_but_wrong_bounds):-
    edge((NC,R)),
    edge((NB,R)),
    node_tag(NC, body_choice),
    node_tag(NB, bounds_correct_atom).

node_tag(R, nl("Can't have the choice condition and not fulfill the bounds")):-
    node_tag(R, choice_condition_but_wrong_bounds).
