% Creates the graph based on the causes and inhibitors

%=== Nodes
node(Atom):-_f_atom(W, Atom).
attr(node,Atom,origin,W):- _f_atom(W, Atom).
attr(node,Atom,abduced,X):- node(Atom), _abduced(X,Atom).
attr(node,Atom,query,X):- node(Atom), _query(X,Atom).

%=== Edges
edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).

edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).
