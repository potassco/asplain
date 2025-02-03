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

%=== Nodes
node(A):-_f_atom(W, A).
attr(node,A,origin,W):- _f_atom(W, A).
attr(node,A,abduced,X):- node(A), _abduced(X,A).
attr(node,A,query,X):- node(A), _query(X,A).

%=== Edges
edge(Cause,Effect,((Cause,Effect),(RuleID,VARS))):-_direct_cause((RuleID,VARS), W, Effect, Cause).
attr(edge,((Cause,Effect),(RuleID,VARS)),origin,W):-_direct_cause((RuleID,VARS), W, Effect, Cause).
% attr(edge,((Cause,Effect),(RuleID,VARS)),rule,RuleID):-_direct_cause((RuleID,VARS), W, Effect, Cause).

edge(Cause,Effect,((Cause,Effect),(RuleID,VARS))):-_direct_inhibitor((RuleID,VARS), W, Effect, Cause), node(Effect), node(Cause).
attr(edge,((Cause,Effect),(RuleID,VARS)),type,inhibitor):-_direct_inhibitor((RuleID,VARS), W, Effect, Cause), node(Effect), node(Cause).
attr(edge,((Cause,Effect),(RuleID,VARS)),type,cause):- _direct_cause((RuleID,VARS), W, Effect, Cause).

in_both(A) :- _f_atom(real, A), _f_atom(hypothetical, A).

r_edge(I1, I2, ((I1,I2),(C_Num,Vars))) :-
    _model_negators(C_Num, Vars, I1, I2), % We take those that interact in integrity constraints.
    not in_both(I1), not in_both(I2),
    _f_atom(real,I1), _f_atom(hypothetical,I2),  % We force one direction only
    node(I1), node(I2).

edge(I1, I2, EID) :- r_edge(I1, I2, EID).
attr(edge, EID, type, reciprocal_inhibitor) :- r_edge(I1, I2, EID).
% attr(edge, ((I1,I2),(C_Num,Vars)), rule, (C_Num,Vars)) :- r_edge(I1, I2, ((I1,I2),(C_Num,Vars))).
attr(edge, ((I1,I2),(C_Num,Vars)), rule_id, C_Num) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).
attr(edge, ((I1,I2),(C_Num,Vars)), rule_str, LABEL) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).
attr(edge, ((I1,I2),(C_Num,Vars)), rule_vars, Vars) :- edge(I1, I2, ((I1,I2),(C_Num,Vars))), _rule(C_Num, LABEL).
