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



fired_edge((atom(A),rule(H,B))):- node_tag(atom(A),true(_)), edge_attr((atom(A),rule(H,B)),type,positive).
fired_edge((atom(A),rule(H,B))):- not node_tag(atom(A),true(_)), edge_attr((atom(A),rule(H,B)),type,negative).
node_tag(rule(H,B), constraint_wouldve_fired):-node_tag(rule(H,B),constraint),
    fired_edge((atom(A),rule(H,B))): edge((atom(A),rule(H,B))).



% --------- Idea to handle the possible invalid bounds

node_tag(rule(H,sum(B,G)), constraint_wouldve_fired):-
    node(rule(H,sum(B,G))), fired(sum(B,G)), not node_tag(rule(H,sum(B,G)),true(_)).

_my_w_literal_tuple(B,A,pos,W):-
    edge_attr((atom(A),rule(H,sum(B,G))), weight, W),
    edge_attr((atom(A),rule(H,sum(B,G))), type, positive).
_my_w_literal_tuple(B,A,neg,W):-
    edge_attr((atom(A),rule(H,sum(B,G))), weight, W),
    edge_attr((atom(A),rule(H,sum(B,G))), type, negative).

fired(sum(B,G)) :- node(rule(H,sum(B,G))),
    #sum { W,A : node_tag(atom(A),true(_)), _my_w_literal_tuple(B, A, pos, W) ;
           W,A : not node_tag(atom(A),true(_)), _my_w_literal_tuple(B, A, neg, W) } >= G.
