node(N):- node(N,reference).
node(N):- node(N, hypothetical).

edge((N1,N2)):- edge((N1,N2),reference).
edge((N1,N2)):- edge((N1,N2),hypothetical).


node_tag(N,true(reference)):- node_tag(N,true,reference).
node_tag(N,true(hypothetical)):- node_tag(N,true,hypothetical).
node_tag(N,T):- node_tag(N,T,hypothetical).
edge_attr((N1,N2),A,V):- edge_attr((N1,N2),A,V,reference).
edge_attr((N1,N2),A,V):- edge_attr((N1,N2),A,V,hypothetical).

#include "show.lp".

explanation_type(hypothetical):- node_tag(N, abduced(_)).
explanation_type(causal):- #false: node_tag(N, true(hypothetical)), not node_tag(N,true(reference));
                         #false: not node_tag(N, true(hypothetical)), node_tag(N,true(reference)).
explanation_type(alternative):- not explanation_type(causal), not node_tag(_, abduced(_)).
#show explanation_type/1.
