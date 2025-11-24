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
% === OUTPUT CONFIG ===
% show_nl. %Show natural langue tet
% show_normal. %Show text normal vs sum
% abducible_dotted. %Abducible rules are dotted
% show_title.
% tuple_body_id.

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
% % color_set(reference, _color_green).
% % color_set(reference,  @concat(_color_green,"35")).
color_set(hypothetical, _color_green).
% % color_set(union, @concat(_color_green,"80")).
% % color_set(union, @concat(_color_green,"85")).
color_set(union, "#36B37E;0.5:#6554C080").
color_set(ref_hypo, @concat(_color_purple,"25")).
color_set(hypo_ref, _color_green).
color_set(edge, blue).
color_set(edge_old, red).
color_set(light, gray84).
color_set(fired_cons, @concat(_color_red,"25")).


% graph(explanation).
% v_graph(G,explanation):- node(N), draw(G).
% v_graph(contrastive,explanation):-draw(contrastive).

attr(graph,default,labelloc,"t").
attr(graph,default,label,"<<b>{{name}}</b><br/>{{description}}>"):-show_title.
attr(graph,default,(label,name),T):-title(T),show_title.
attr(graph,default,(label,description),@format("({})",T)):-explanation_type(T),show_title.
attr(graph,default,fontname,"Baskerville").
attr(graph,default,fontsize,"20").

attr(node,N,style,filled):- node(N), not node_tag(N, abducible(_)).
attr(node,N,style,"filled,dashed"):- node(N), node_tag(N, abducible(_)), abducible_dotted.
attr(node,N,fontname,"Baskerville"):-  node(N).

attr(node,N,tooltip,@format(S,P)):- node(N), node_tag(N,nl(S,P)).

% ## Nodes
attr(node,rule(H,B),shape,box):-node(rule(H,B)).

% attr(node,rule(H,B),label,"<<u><font point-size=\"9\">{{input}}</font> </u><br/> BODY {{value}} <br/><i>{{nl}} </i><br/> <u><font point-size=\"9\">{{output}}</font></u>>"):-
attr(node,rule(H,B),label,"<<font point-size=\"9\">{{input}} </font><br/> BODY {{value}} <br/><i>{{nl}} </i>{{nlbr}} <u><font point-size=\"9\">{{output}}</font></u>>"):-
    node(rule(H,B)), not node_tag(rule(H,B),disabled).
attr(node,rule(H,B),label,"<<font point-size=\"9\">{{input}} </font><br/><s> BODY {{value}} </s><br/><i>{{nl}} </i>{{nlbr}} <u><font point-size=\"9\">{{output}}</font></u>>"):-
    node(rule(H,B)), node_tag(rule(H,B),disabled).
% attr(node,(rule(H,B)),label,"<{{input}}<br/> BODY {{value}} <br/>{{output}}>"):-
%     node((rule(H,B))).

id(rule(disjunction(H),normal(B)),(H,B)):-node(rule(disjunction(H),normal(B))),tuple_body_id.
id(rule(choice(H),normal(B)),(H,B)):-node(rule(choice(H),normal(B))),tuple_body_id.
id(rule(disjunction(H),sum(B,W)),(H,B)):-node(rule(disjunction(H),sum(B,W))),tuple_body_id.
id(rule(choice(H),sum(B,W)),(H,B)):-node(rule(choice(H),sum(B,W))),tuple_body_id.

id(rule(H,normal(B)),B):-node(rule(H,normal(B))), not tuple_body_id.

attr(node,(N),(label,nl),@format(S,P)):-
    node((N)),node_tag(N,nl(S,P)),show_nl.
attr(node,(N),(label,nlbr),"<br/>"):-
    node((N)),show_nl.
attr(node,rule(H,B),(label,value),ID):-
    node(rule(H,B)),id(rule(H,B),ID).
attr(node,rule(choice(H),B),(label,output),"choice"):-
    node(rule(choice(H),B)).
attr(node,rule(disjunction(H),B),(label,output),"disjunction"):-
    node(rule(disjunction(H),B)).
attr(node,rule(H,normal(B)),(label,input),"normal"):-
    node(rule(H,normal(B))),show_normal.
attr(node,rule(H,sum(B,W)),(label,input),@concat("sum at least ",W)):-
    node(rule(H,sum(B,W))),show_normal.

attr(node, atom(A), label, "<{{atom}}{{nlbr}}<i>{{nl}} </i>>"):- node(atom(A)).
attr(node, atom(A), (label,atom), A):- node(atom(A)).
attr(node, atom(A), (label,nl), @format(L,P)):- node(atom(A)), node_tag(atom(A), nl(L,P)), show_nl.
attr(node, atom(A), (label,nlbr), "<br/>"):- node(atom(A)),  show_nl.


% ## Edges
attr(edge,((A),(R)),style,dashed):- edge_attr((A,R), type, negative).
attr(edge,((A),(R)),style,dashed):- edge_attr((A,R), type, negative).
attr(edge,((A),(R)),label,W):- edge_attr((A,R), weight, W).

attr(edge,((atom(A)),(rule(H,B))),arrowhead,none):- edge(((atom(A)),(rule(H,B)))).
% attr(edge,((rule(H,B)),(atom(A))),color,orange):- v_edge(((rule(H,B)),(atom(A))),_).


% attr(edge,((A,contrastive),(R,contrastive)),style,dashed):- edge_attr((A,R), type, negative).
% attr(edge,((A,contrastive),(R,contrastive)),label,W):- edge_attr((A,R), weight, W).

% ## Highlight model
true_node(N):- node_tag(N,true).

active_node(N):- draw_type(pg), node(N), not node_tag(N,disabled).
active_node(atom(A)):- draw_type((model;explanation)), node(atom(A)),node_tag(atom(A),true). %All atoms are active in the model.
active_node(rule(H,B)):- draw_type((model;explanation)), node(rule(H,B)), true_node(rule(H,B)). % Only true rules are active
% active_node(rule(H,B)):- draw_type((model;explanation)), node(rule(H,B)), not node_tag(rule(H,B),disabled). % Only true rules are active
% TODO define when a node is active in explanation option


active_edge(((A),(B))):- draw_type(pg), edge((A,B)),not node_tag(A,disabled).
active_edge(((A),(B))):- draw_type(model), edge((A,B)), active_node((A)), active_node((B)), true_node((B)).
active_edge(((A),(B))):- draw_type(explanation), edge((A,B)), reason((A,B)).
active_edge(((atom(A)),(B))):- draw_type(explanation), edge((atom(A),B)), true_node((B)).


% active_edge(((atom(A)),(rule(H,B)))):- draw_type(model), edge_attr((atom(A),rule(H,B)), type, positive,_), true_node((atom(A))).
% active_edge(((atom(A)),(rule(H,B)))):- draw_type(model), edge_attr((atom(A),rule(H,B)), type, negative,_), not true_node((atom(A))), graph(G).
% active_edge(((rule(H,B)),(atom(A)))):- draw_type(model), true_node((rule(H,B))),edge((rule(H,B),atom(A))).


attr(node,N,fillcolor,C):-node(N), true_node(N), color_set(G,C), not draw_type(pg), graph_type(G).
attr(node,N,fillcolor,white):-node(N), draw_type(pg).
attr(node,N,fillcolor,white):-node(N), not true_node(N), not draw_type(contrast) .

attr(node,N,fillcolor, C):-node_tag(N,true(reference)), node_tag(N,true(hypothetical)), color_set(union, C),draw_type(contrast).
attr(node,N,fillcolor, C):-node_tag(N,true(hypothetical)), not node_tag(N, true(reference)) ,color_set(hypo_ref,C),draw_type(contrast).
attr(node,N,fillcolor, C):-not node_tag(N,true(hypothetical)), node_tag(N, true(reference)), color_set(ref_hypo,C),draw_type(contrast).
attr(node,N,fillcolor, white):-node(N), not node_tag(N,true(hypothetical)), not node_tag(N, true(reference)), not node_tag(N, constraint_wouldve_fired),draw_type(contrast).
attr(node,N,fillcolor, C):-node(N), node_tag(N,constraint_wouldve_fired),draw_type(contrast),color_set(fired_cons, C).

attr(node,N,penwidth, "4"):-node_tag(N,query(_)).



attr(node,N,(fontcolor;color),C):- node(N),
                                not active_node(N),
                                color_set(light,C),
                                not node_tag(N,abduced(_)).

attr(node,R,(fontcolor;color),red):- node_tag(R,abduced(rm)).
attr(node,R,(fontcolor;color),blue):- node_tag(R,abduced(add)).


attr(edge,((N1),(N2)),color,C):-edge((N1,N2)), not active_edge(((N1),(N2))), color_set(light,C).


% cons(rule(disjunction(H),B)):-
%     node(rule(disjunction(H),B)), %rule node
%     not edge((rule(disjunction(H),B),atom(_))). % no outgoing edges
% fired_edge((atom(A),rule(H,B))):- node_tag(atom(A),true(_)), edge_attr((atom(A),rule(H,B)),type,positive).
% fired_edge((atom(A),rule(H,B))):- not node_tag(atom(A),true(_)), edge_attr((atom(A),rule(H,B)),type,negative).
% node_tag(r, constraint_ule(H,B)):-cons(rule(H,B)),
%     fired_edge((atom(A),rule(H,B))): edge((atom(A),rule(H,B))).




% attr(node,X,id,X):-node(X).



% linked_element(node,X,X):-node(X).
% linked_element(node,Y,X):-edge((X,Y)).
% linked_element(edge,(X,Y),X):-edge((X,Y)).
% linked_element(edge,(X,Y),Y):-edge((X,Y)).


% % attr(node,X,class,@svg_init("visibility","hidden")):-node(X),not root(X).
% % attr(edge,(X,Y),class,@svg_init("visibility","hidden")) :- edge((X,Y)).


% attr(Type,E,class,@svg("click",X,"visibility","visible")):-linked_element(Type,E,X).
% attr(Type,E,class,@svg("mouseenter",X,"opacity","1")):-linked_element(Type,E,X).
% attr(Type,E,class,@svg("mouseleave",X,"opacity","0.2")):-linked_element(Type,E,X).
