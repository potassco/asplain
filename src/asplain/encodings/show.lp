#show node/1.
#show edge/1.
#show edge_attr/3.
#show node_tag/2.

#show hold/1.
#show body/1.
% #show abduced/2.
% #show query/2.
#defined abduced/2.
#show node_tag(R,abduced(T)): abduced(T,R).
#show node_tag(atom(A),query(T)): query(T,A).

#show node_tag(N,true): hold(N).

#show fail_query/0.
