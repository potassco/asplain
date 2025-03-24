%*

Creates the graph based on the causes and inhibitors

#node(A)
    Defines a node in the graph
    - A: the node identifier (atom)

#edge(N,N',ID)
    Defines an edge in the graph. They represent the causal relationships between nodes,
    as well as negative relationships (inhibitors).
    - N: the origin node
    - N': the destination node
    - ID: the identifier of the edge (Required for muli-edges)

#attr(T,N,A,V)
    Defines an attribute for a node or edge.

    - T: the type of the element (`node` or `edge`)
    - N: the node or edge identifier
    - A: the attribute name
    - V: the attribute value

    === "T=`node`"

        - `A=origin`: `V` = either `real` or `hypothetical`
        - `A=abduced`: `V` = either `rm` or `add`
        - `A=query`: `V` = either `include` or `exclude`

    === "T=`edge`"

        - `A=origin`: `V` = either `real` or `hypothetical`
        - `A=type`: `V` = either `inhibitor` or `cause`

*%

% visible(Atom) :- _abduced(_,Atom).
% visible(Atom) :- _query(_,Atom).
% visible(Atom) :- _visible(Atom).
% visible(Atom) :- _f_atom(W,Atom), not in_both(Atom).

% visible(person(gabriel)).
% visible(person(clare)).

visible(alcohol(clare)).
visible(alcohol(gabriel)).
visible(drive(gabriel)).
visible(drive(clare)).
visible(resist(gabriel)).
visible(resist(clare)).

% visible(punish(gabriel)).
% visible(punish(clare)).

% visible(sentence(gabriel,prison)).
% visible(sentence(clare,innocent)).
% visible(sentence(gabriel, innocent)).

visible(loved(gabriel)).
visible(hated(gabriel)).
visible(glory(gabriel)).
visible(loved(clare)).
visible(hated(clare)).
visible(glory(clare)).

tab(cause,     cause,     cause).
tab(cause,     inhibitor, inhibitor).
tab(inhibitor, cause,     inhibitor).
tab(inhibitor, inhibitor, enabler).
tab(enabler,   inhibitor, inhibitor).

%
_skip(World, (RID,Vars), (Cause, Effect), cause) :- _direct_cause((RID, Vars), World, Effect, Cause), not visible(Cause).
_skip(World, (RID,Vars), (Cause, Effect), cause) :- _direct_cause((RID, Vars), World, Effect, Cause), not visible(Effect).
%
_reach(World, (RID, Vars), (X, Y), cause) :- _direct_cause((RID, Vars), World, Y, X), not _skip(World, (RID,Vars), (X, Y), cause).  % Base
_reach(World, RULE, (Cause, TransitiveEffect), cause) :- _skip(World, RULE, (Cause, TransitiveEffect), cause).  % Base
_reach(World, RULE, (X, Z), cause) :-       % transitivity
    _reach(World, RULE, (X, Y), cause),     
    skip(World, RULE, (Y, Z), cause).  
%

%  Contrastive skips
_skip(contrastive, (RID,Vars), (Cause, Effect), cause) :- _skip(World, (RID,Vars), (Cause, Effect), cause).  % Inherit skips from other two graphs
%
_skip(contrastive, (RID,Vars), (Inhibitor, Effect), inhibitor) :-     % skip inhibitor if one of the ends is not visible
    _direct_inhibitor((RID, Vars), World1, Effect, Inhibitor),   % Effect its true in World1, Inhibitor inhibits it in World2
    _f_atom(World1, Effect), _f_atom(World2, Inhibitor), World1 != World2,
    not visible(Inhibitor).
_skip(contrastive, (RID,Vars), (Inhibitor, Effect), inhibitor) :- 
    _direct_inhibitor((RID, Vars), World1, Effect, Inhibitor),   
    _f_atom(World1, Effect), _f_atom(World2, Inhibitor), World1 != World2,
    not visible(Effect).
%

% Contrastive reach
%
_reach(contrastive, RULE, (X, Y), cause) :-       % Inherit causes from other two graphs
    _reach(_, RULE, (X, Y), cause).
%
_reach(contrastive, (RID, Vars), (Inhibitor, Effect), inhibitor) :-   % include the edge if not skip
    _direct_inhibitor((RID, Vars), World1, Effect, Inhibitor),   % Effect its true in World1, Inhibitor inhibits it in World2
    _f_atom(World1, Effect), _f_atom(World2, Inhibitor), World1 != World2,
    not _skip(contrastive, (RID,Vars), (Inhibitor, Effect), inhibitor).  % Base
%
_reach(contrastive, RULE, (Cause, TransitiveEffect), inhibitor) :- _skip(contrastive, RULE, (Cause, TransitiveEffect), inhibitor).  % Base
%
_reach(contrastive, RULE2, (X, Z), FinalType) :-       % transitivity
    _reach(contrastive, RULE, (X, Y), Type1),     
    _skip(contrastive, RULE2, (Y, Z), Type2),
    tab(Type1, Type2, FinalType).  
%

%
_edge(World, RULE, (X, Y), Type) :- visible(X), visible(Y), _reach(World, RULE, (X, Y), Type).
_node(World, Atom) :- _f_atom(World, Atom), visible(Atom).
_node(contrastive, Atom) :- _f_atom(World, Atom), visible(Atom).
%

%=== Nodes
node(A):- _node(World,A).
attr(node,A,origin,W):- _node(W,A).
attr(node,A,abduced,X):- node(A), _abduced(X,A).
attr(node,A,query,X):- node(A), _query(X,A).

%=== Edges
edge(Cause,Effect,((Cause,Effect),(RuleID,VARS))):-       _edge(W, (RuleID,VARS), (Cause, Effect), Type).
attr(edge,((Cause,Effect),(RuleID,VARS)),origin,W):-      _edge(W, (RuleID,VARS), (Cause, Effect), Type).
attr(edge,((Cause,Effect),(RuleID,VARS)),rule,RuleID):-   _edge(W, (RuleID,VARS), (Cause, Effect), Type).
attr(edge,((Cause,Effect),(RuleID,VARS)),type,Type):-     _edge(W, (RuleID,VARS), (Cause, Effect), Type).

% in_both(A) :- _f_atom(real, A), _f_atom(hypothetical, A).

% r_edge(I1, I2, ((I1,I2),(C_Num,Vars))) :-
%     _model_negators(C_Num, Vars, I1, I2), % We take those that interact in integrity constraints.
%     not in_both(I1), not in_both(I2),
%     _f_atom(real,I1), _f_atom(hypothetical,I2),  % We force one direction only
%     node(I1), node(I2).

% edge(I1, I2, EID) :- r_edge(I1, I2, EID).
% attr(edge, EID, type, reciprocal_inhibitor) :- r_edge(I1, I2, EID).
% % attr(edge, ((I1,I2),(C_Num,Vars)), rule, (C_Num,Vars)) :- r_edge(I1, I2, ((I1,I2),(C_Num,Vars))).
% attr(edge, ((I1,I2),(C_Num,Vars)), rule_id, C_Num) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).
% attr(edge, ((I1,I2),(C_Num,Vars)), rule_str, LABEL) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).
% attr(edge, ((I1,I2),(C_Num,Vars)), rule_vars, Vars) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).