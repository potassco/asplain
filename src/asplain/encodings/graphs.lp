%*

Creates the graph based on the causes and inhibitors

#node(A)
    Defines a node in the graph
    - A: the node identifier (atom)

#edge(N,N')
    Defines an edge in the graph. They represent the causal relationships between nodes,
    as well as negative relationships (inhibitors).
    - N: the origin node
    - N': the destination node

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
edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).

edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).
