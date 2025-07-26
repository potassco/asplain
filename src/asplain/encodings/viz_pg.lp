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

% ====================
% === CONFIGURATION===
% Now passed when the program is called


% draw(contrastive).
% draw(hypothetical).
% draw(reference).

% draw_type(pg).
% draw_type(model).
% draw_type(explanation).
% ====================



color_set(reference, @concat(_color_purple,"80")).
% color_set(reference, _color_green).
% color_set(reference,  @concat(_color_green,"35")).
color_set(hypothetical, _color_green).
% color_set(union, @concat(_color_green,"80")).
% color_set(union, @concat(_color_green,"85")).
color_set(union, "#36B37E;0.5:#6554C080").
color_set(ref_hypo, @concat(_color_purple,"25")).
color_set(hypo_ref, _color_green).
color_set(edge, blue).
color_set(edge_old, red).
color_set(light, gray84).
color_set(fired_cons, @concat(_color_red,"25")).

graph((reference;hypothetical;contrastive)).
type_hypothetical(hypothetical):-node(N,reference), not node(N,hypothetical).
type_hypothetical(hypothetical):-node(N,hypothetical), not node(N,reference).
type_hypothetical(alternative):- not type_hypothetical(same), #false:  node(N,reference), not node(N,hypothetical);#false:  node(N,hypothetical), not node(N,reference).
type_hypothetical(same):- #false: hold(A, hypothetical), not hold(A,reference);
                         #false: not hold(A, hypothetical), hold(A,reference).



v_graph(explanation).
v_graph(G,explanation):- node(N,G), draw(G).
v_graph(contrastive,explanation):-draw(contrastive).

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

v_node((N,G),G):- node(N,G),draw(G).
v_edge(((N1,G),(N2,G)),G):- edge((N1,N2),G),draw(G).
v_attr(node,(N,G),style,filled):- v_node((N,G),G).
v_attr(node,(N,G),fontname,"Baskerville"):- v_node((N,G),G).

% ## Nodes
v_attr(node,(rule(H,B),G),shape,box):-v_node((rule(H,B),G),G).
v_attr(node,(rule(H,B),G),label,"<<i>{{input}} </i><br/> BODY {{value}} <br/><u>{{nl}} </u><br/> <i>{{output}}</i>>"):-
    v_node((rule(H,B),G),G).
% v_attr(node,(rule(H,B),G),label,"<{{input}}<br/> BODY {{value}} <br/>{{output}}>"):-
%     v_node((rule(H,B),G),G).

id(rule(disjunction(H),normal(B)),(H,B)):-node(rule(disjunction(H),normal(B)),_).
id(rule(choice(H),normal(B)),(H,B)):-node(rule(choice(H),normal(B)),_).
id(rule(disjunction(H),sum(B,W)),(H,B)):-node(rule(disjunction(H),sum(B,W)),_).
id(rule(choice(H),sum(B,W)),(H,B)):-node(rule(choice(H),sum(B,W)),_).

v_attr(node,(N,G),(label,nl),@format(S,P)):-
    v_node((N,G),G),node_tag(N,nl(S,P)).

v_attr(node,(rule(H,B),G),(label,value),ID):-
    v_node((rule(H,B),G),G),id(rule(H,B),ID).
% v_attr(node,(rule(H,normal(B)),G),(label,value),B):-
%     v_node((rule(H,normal(B)),G),G).
% v_attr(node,(rule(H,sum(B,G)),G),(label,value),B):-
%     v_node((rule(H,sum(B,G)),G),G).
v_attr(node,(rule(choice(H),B),G),(label,output),"choice"):-
    v_node((rule(choice(H),B),G),G).
v_attr(node,(rule(disjunction(H),B),G),(label,output),"disjunction"):-
    v_node((rule(disjunction(H),B),G),G).
v_attr(node,(rule(H,normal(B)),G),(label,input),"normal"):-
    v_node((rule(H,normal(B)),G),G).
v_attr(node,(rule(H,sum(B,W)),G),(label,input),@concat("sum at least ",W)):-
    v_node((rule(H,sum(B,W)),G),G).

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

active_node((N,G)):- draw_type(pg), node(N,G).
active_node((atom(A),G)):- draw_type((model;explanation)), node(atom(A), G). %All atoms are active in the model.
active_node((rule(H,B),G)):- draw_type((model;explanation)), node(rule(H,B),G), true_node((rule(H,B),G)). % Only true rules are active
% TODO define when a node is active in explanation option


active_edge(((A,G),(B,G))):- draw_type(pg), edge((A,B),G).
active_edge(((A,G),(B,G))):- draw_type(model), edge((A,B),G), active_node((A,G)), active_node((B,G)), true_node((B,G)).
active_edge(((A,G),(B,G))):- draw_type(explanation), edge((A,B),G), reason((A,B),G).
active_edge(((atom(A),G),(B,G))):- draw_type(explanation), edge((atom(A),B),G), true_node((B,G)).


% active_edge(((atom(A),G),(rule(H,B),G))):- draw_type(model), edge_attr((atom(A),rule(H,B)), type, positive,_), true_node((atom(A),G)).
% active_edge(((atom(A),G),(rule(H,B),G))):- draw_type(model), edge_attr((atom(A),rule(H,B)), type, negative,_), not true_node((atom(A),G)), graph(G).
% active_edge(((rule(H,B),G),(atom(A),G))):- draw_type(model), true_node((rule(H,B),G)),edge((rule(H,B),atom(A)),G).


v_attr(node,(N,G),fillcolor,C):-node(N, G), true_node((N,G)), color_set(G,C), not draw_type(pg).
v_attr(node,(N,G),fillcolor,white):-node(N, G), draw_type(pg).
v_attr(node,(N,G),fillcolor,white):-node(N, G), not true_node((N,G)).

v_attr(node,(N,G),(fontcolor;color),C):- node(N,G),
                                not active_node((N,G)),color_set(light,C).

v_attr(edge,((N1,G),(N2,G)),color,C):-edge((N1,N2),G), not active_edge(((N1,G),(N2,G))), color_set(light,C).
% v_attr(edge,((N1,contrastive),(N2,contrastive)/),color,C):-edge((N1,N2),hypothetical), color_set(light,C).


% ## Highlight explanation
% v_attr(edge,((N1,G),(atom(A),G)),color,C):-reason((N1,atom(A)),G), color_set(edge, C).
% v_attr(edge,((N1,G),(atom(A),G)),color,gray80):-edge((N1,atom(A)),G),not reason((N1,atom(A)),G), color_set(edge, C).
% v_attr(edge,((N1,contrastive),(atom(A),contrastive)),color,C):-reason((N1,atom(A)),hypothetical), color_set(edge, C).

% ## Highlight query
% v_attr(node,(atom(A),(reference;contrastive)),penwidth, "10"):-_input(A,_).
% v_attr(node,(atom(A),(reference)),color, "green"):-_input(A,true).
% v_attr(node,(atom(A),(reference)),color, "red"):-_input(A,false).
% v_attr(node,(atom(A),(hypothetical)),penwidth, "10"):-_input(A,_), not _abduced(_, A).
% v_attr(node,(atom(A),(contrastive;hypothetical;reference)),fillcolor, "black"):-_abduced(_,A).

% ----------------------------------------
% ## Contrastive
% v_attr(node,(N,contrastive),penwidth,"4"):- node(N,reference), not node(N,hypothetical).
% v_node((N,contrastive),contrastive):- node(N,G), draw(contrastive).

% This idea of hiding does not work well with causal explanation where the query was already true.
hide_rule(rule(H,B)):- node(rule(H,B),G), true_node((rule(H,B),reference)),true_node((rule(H,B),hypothetical)), H=disjunction(H'),not _abduced(rm,rule(H,B)).
hide_rule(rule(H,B)):- node(rule(H,B),G), not true_node((rule(H,B),reference)), not true_node((rule(H,B),hypothetical)), not rule_could_have_fired(rule(H,B)),not _abduced(rm,rule(H,B)).

v_node((atom(N),contrastive),contrastive):- node(atom(N),G), draw(contrastive).
v_node((rule(H,B),contrastive),contrastive):- node(rule(H,B),G), draw(contrastive), not hide_rule(rule(H,B)). %Hide rule nodes that aare never true
v_edge(((N1,contrastive),(N2,contrastive)),contrastive):- edge((N1,N2),G), draw(contrastive), v_node((N1,contrastive),contrastive), v_node((N2,contrastive),contrastive).

% v_attr(node,(N,contrastive),(fontcolor;color),red):- node(N,reference), not node(N,hypothetical).
v_attr(node,(rule(H,B),contrastive),(fontcolor;color),red):- _abduced(rm,rule(H,B)).
v_attr(node,(rule(H,B),contrastive),(fontcolor;color),blue):- _abduced(add,rule(H,B)).
v_attr(node,(N,contrastive),(fontcolor;color),C):- node(N,hypothetical),
                                not true_node((N,hypothetical)), color_set(light, C), v_node((N,contrastive),contrastive).
                                % true_node((N,reference)).


v_attr(node,(N,contrastive),label,L):- v_attr(node,(N,G),label,L),v_node((N,contrastive),contrastive).
v_attr(node,(N,contrastive),(label,K),L):- v_attr(node,(N,G),(label,K),L),v_node((N,contrastive),contrastive).


v_attr(node,(N,contrastive),fillcolor, C):-true_node((N, hypothetical)),true_node((N, reference)), color_set(union, C).
v_attr(node,(N,contrastive),fillcolor, C):-true_node((N, hypothetical)), not true_node((N, reference)),color_set(hypo_ref,C).
v_attr(node,(N,contrastive),fillcolor, C):-not true_node((N, hypothetical)), true_node((N, reference)), color_set(ref_hypo,C).
v_attr(node,(N,contrastive),fillcolor, white):-v_node((N,contrastive),contrastive), not true_node((N, hypothetical)), not true_node((N, reference)), not rule_could_have_fired(N).
v_attr(node,(atom(A),contrastive),penwidth, "4"):-_query(_,A).

v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-edge((N1,N2),hypothetical), not active_edge(((N1,hypothetical),(N2,hypothetical))), color_set(light,C).
v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-edge((N1,N2),reference), not edge((N1,N2),hypothetical), color_set(light,C).
v_attr(edge,((N1,contrastive),(atom(A),contrastive)),color,C):-edge((N1,atom(A)),hypothetical),not reason((N1,atom(A)),hypothetical), color_set(light, C).


_cons(rule(disjunction(H),B)):-
    node(rule(disjunction(H),B),hypothetical), %rule node
    not edge((rule(disjunction(H),B),atom(_)),hypothetical). % no outgoing edges
rule_could_have_fired(rule(H,B)):-_cons(rule(H,B)),
    #false: edge((atom(N),rule(H,B)),hypothetical), not true_node((atom(N),hypothetical)), not true_node((atom(N),reference)). %All literals are true in at least one model.
% rule_could_have_fired(rule(H,B)):-_cons(rule(H,B),atom(_)), true_node(atom(N),_): edge((atom(N),rule(H,B))).

v_attr(node,(N,contrastive),fillcolor, C):-v_node((N,contrastive),contrastive), rule_could_have_fired(N), color_set(fired_cons, C).


% ## Highlight difference
% v_attr(edge,((N1,contrastive),(N2,contrastive)),color,C):-reason((N1,N2),reference), not reason((N1,N2), hypothetical),color_set(edge_old,C), true_node((N1,hypothetical)).



% _contrast_lt(B):-node(rule(H,normal(B)),_).
% _contrast_lt(B,A,pos):-edge_attr((atom(A),rule(H,normal(B))), type, positive,_).
% _contrast_lt(B,A,neg):-edge_attr((atom(A),rule(H,normal(B))), type, negative,_).
% _contrast_conjunction(B) :- _contrast_lt(B),
%     hold(A) : _contrast_lt(B, A, pos);
%     not hold(A) : _contrast_lt(B, A, neg).
% _contrast_body(normal(B)) :- node(rule(_,normal(B)),_), _contrast_conjunction(B).
% v_attr(node,(rule(H,normal(B)),contrastive),color, red):-node(rule(H,normal(B)),_),_contrast_body(normal(B)), not true_node((rule(H,normal(B)),_)).
