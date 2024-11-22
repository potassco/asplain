graph((real;hypothetical;contrastive)).
node(Atom, World):-_f_atom(World, Atom).
edge((Cause,Effect),World):-_direct_cause(RuleID, World, Effect, Cause).

node(Atom, contrastive):- node(Atom, (real;hypothetical)).
attr(node,Atom,abduced,X):- node(Atom, W), _abduced(X,Atom).

edge((Cause,Effect),contrastive):-_direct_inhibitor(RuleID, World, Effect, Cause).
edge((Cause,Effect),contrastive):-_direct_cause(RuleID, World, Effect, Cause).
attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, World, Effect, Cause).
attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, World, Effect, Cause).
% attr(edge,(Cause,Effect),origin,World):-_direct_cause(RuleID, World, Effect, Cause).
