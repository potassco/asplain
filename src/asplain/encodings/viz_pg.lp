% Visualizes the program graph using clingraph
% --------------------------------------------------------

#include "reify_defined.lp".
#const _color_blue = "#0052CC50".
#const _color_green = "#36B37E".
#const _color_orange = "#FFAB0050".
#const _color_red = "#FF5630".
#const _color_gray = "#B3BAC550".
#const _color_light = "#B3BAC560".
#const _color_purple = "#6554C0".
#const _color_both = "#57B5BD50".

% color_set(reference, _color_green).
color_set(reference, _color_green).
color_set(hypothetical, _color_green).
% color_set(union, @concat(_color_green,"80")).
color_set(union, @concat(_color_green,"70")).
color_set(ref_hypo, @concat(_color_green,"15")).
color_set(hypo_ref, _color_green).
color_set(edge, blue).
color_set(edge_old, red).
color_set(light, gray80).

graph((reference;hypothetical;contrastive)).
type_hypothetical(hypothetical):-node(N,reference), not node(N,hypothetical).
type_hypothetical(alternative):- not type_hypothetical(same), #false:  node(N,reference), not node(N,hypothetical).
type_hypothetical(same):- #false: hold(A, hypothetical), not hold(A,reference);
                         #false: not hold(A, hypothetical), hold(A,reference).



v_graph(explanation).
v_graph(G,explanation):- node(N,G).
v_graph(contrastive,explanation).

v_attr(graph,(reference;hypothetical),label,"<<b>{{name}}</b><br/>({{type}})>").
v_attr(graph,reference,(label,name),"Reference").
v_attr(graph,reference,(label,type),"Real").
v_attr(graph,hypothetical,(label,name),"Found").
v_attr(graph,hypothetical,(label,type),@stringify(T,true)):-type_hypothetical(T).
v_attr(graph,contrastive,label,"<<b>Contrastive</b><br/><br/>>"):-graph(contrastive).
v_attr(graph,G,fontname,"Baskerville"):-v_graph(G,_).
v_attr(graph,G,fontsize,"20"):-v_graph(G,_).
% v_attr(graph,G,fontname,"Baskerville"):-graph(G).
% v_attr(graph,hypothetical,label,"<<b>Hypothetical</b>>"):- node(N,G).
% v_attr(graph,reference,label,"<<b>Reference</b>>"):- node(N,G).

v_node((N,G),G):- node(N,G).
v_edge(((N1,G),(N2,G)),G):- edge((N1,N2),G).
v_edge(((N1,contrastive),(N2,contrastive)),contrastive):- edge((N1,N2),G).
v_attr(node,(N,G),style,filled):- v_node((N,G),G).
v_attr(node,(N,G),fontname,"Baskerville"):- v_node((N,G),G).

% ## Nodes
v_attr(node,(rule(H,B),G),shape,box):-v_node((rule(H,B),G),G).
v_attr(node,(rule(H,B),G),label,"<<i>{{input}} </i><br/> BODY {{value}} <br/><i>{{output}}</i>>"):-
    v_node((rule(H,B),G),G).
% v_attr(node,(rule(H,B),G),label,"<{{input}}<br/> BODY {{value}} <br/>{{output}}>"):-
%     v_node((rule(H,B),G),G).
v_attr(node,(rule(H,normal(B)),G),(label,value),B):-
    v_node((rule(H,normal(B)),G),G).
v_attr(node,(rule(H,sum(B,G)),G),(label,value),B):-
    v_node((rule(H,sum(B,G)),G),G).
v_attr(node,(rule(choice(H),B),G),(label,output),"choice"):-
    v_node((rule(choice(H),B),G),G).
v_attr(node,(rule(disjunction(H),B),G),(label,output),"disjuction"):-
    v_node((rule(disjunction(H),B),G),G).
v_attr(node,(rule(H,normal(B)),G),(label,input),"normal"):-
    v_node((rule(H,normal(B)),G),G).
v_attr(node,(rule(H,sum(B,G)),G),(label,input),@concat("sum at least ",G)):-
    v_node((rule(H,sum(B,G)),G),G).

v_attr(node, (atom(A),G), label, A):- node(atom(A), G).

% ## Edges
v_attr(edge,((A,G),(R,G)),style,dashed):- edge_attr((A,R), type, negative, G).
v_attr(edge,((A,G),(R,G)),label,W):- edge_attr((A,R), weight, W, G).

v_attr(edge,((atom(A),G),(rule(H,B),G)),arrowhead,none):- v_edge(((atom(A),G),(rule(H,B),G)),_).
% v_attr(edge,((rule(H,B),G),(atom(A),G)),color,orange):- v_edge(((rule(H,B),G),(atom(A),G)),_).


v_attr(edge,((A,contrastive),(R,contrastive)),style,dashed):- edge_attr((A,R), type, negative, G).
v_attr(edge,((A,contrastive),(R,contrastive)),label,W):- edge_attr((A,R), weight, W, G).


% ## Highlight model
true_node((rule(H,B),G)):- node(rule(H,B), G), body(B,G).
true_node((atom(A),G)):- node(atom(A), G), hold(A,G).
v_attr(node,(N,G),fillcolor,C):-node(N, G), true_node((N,G)), color_set(G,C).
v_attr(node,(N,G),fillcolor,white):-node(N, G), not true_node((N,G)).
active_edge(((atom(A),G),(rule(H,B),G))):- edge_attr((atom(A),rule(H,B)), type, positive,_), true_node((atom(A),G)).
active_edge(((atom(A),G),(rule(H,B),G))):- edge_attr((atom(A),rule(H,B)), type, negative,_), not true_node((atom(A),G)), graph(G).
active_edge(((rule(H,B),G),(atom(A),G))):- true_node((rule(H,B),G)),edge((rule(H,B),atom(A)),G).
v_attr(edge,((N1,G),(N2,G)),color,C):-edge((N1,N2),G), not active_edge(((N1,G),(N2,G))), color_set(light,C).
v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-edge((N1,N2),hypothetical), not active_edge(((N1,hypothetical),(N2,hypothetical))), color_set(light,C).
v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-edge((N1,N2),reference), not edge((N1,N2),hypothetical), color_set(light,C).
% v_attr(edge,((N1,contrastive),(N2,contrastive)/),color,C):-edge((N1,N2),hypothetical), color_set(light,C).


% ## Highlight explanation
v_attr(edge,((N1,G),(N2,G)),color,C):-reason((N1,N2),G), color_set(edge, C).

% ## Highlight query
v_attr(node,(atom(A),contrastive),penwidth, "4"):-_query(_,A).

% ----------------------------------------
% ## Contrastive
% v_attr(node,(N,contrastive),penwidth,"4"):- node(N,reference), not node(N,hypothetical).
v_attr(node,(N,contrastive),(fontcolor;color),red):- node(N,reference), not node(N,hypothetical).
v_attr(node,(N,contrastive),(fontcolor;color),blue):- node(N,hypothetical), not node(N,reference).
v_attr(node,(N,contrastive),(fontcolor;color),gray):- node(N,reference), node(N,hypothetical),
                                not true_node((N,hypothetical)),
                                true_node((N,reference)).


v_node((N,contrastive),contrastive):- node(N,G).
v_attr(node,(N,contrastive),label,L):- v_attr(node,(N,G),label,L).
v_attr(node,(N,contrastive),(label,K),L):- v_attr(node,(N,G),(label,K),L).


v_attr(node,(N,contrastive),fillcolor, C):-true_node((N, hypothetical)),true_node((N, reference)), color_set(union, C).
v_attr(node,(N,contrastive),fillcolor, C):-true_node((N, hypothetical)), not true_node((N, reference)),color_set(hypo_ref,C).
v_attr(node,(N,contrastive),fillcolor, C):-not true_node((N, hypothetical)), true_node((N, reference)), color_set(ref_hypo,C).
v_attr(node,(N,contrastive),fillcolor, white):-v_node((N,contrastive),contrastive), not true_node((N, hypothetical)), not true_node((N, reference)).

% ## Highlight difference
v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-reason((N1,N2),reference), not reason((N1,N2), hypothetical),color_set(edge_old,C), true_node((N1,hypothetical)).



% _contrast_lt(B):-node(rule(H,normal(B)),_).
% _contrast_lt(B,A,pos):-edge_attr((atom(A),rule(H,normal(B))), type, positive,_).
% _contrast_lt(B,A,neg):-edge_attr((atom(A),rule(H,normal(B))), type, negative,_).
% _contrast_conjunction(B) :- _contrast_lt(B),
%     hold(A) : _contrast_lt(B, A, pos);
%     not hold(A) : _contrast_lt(B, A, neg).
% _contrast_body(normal(B)) :- node(rule(_,normal(B)),_), _contrast_conjunction(B).
% v_attr(node,(rule(H,normal(B)),contrastive),color, red):-node(rule(H,normal(B)),_),_contrast_body(normal(B)), not true_node((rule(H,normal(B)),_)).
