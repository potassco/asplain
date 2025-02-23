#const _color_blue = "#0052CC".
#const _color_purple = "#6554C0".
#const _color_green = "#36B37E".
#const _color_gray = "#B3BAC5".
#const _color_yellow = "#FFAB00".
#const _color_red = "#FF5630".

% ===== Graphs
graph((real;hypothetical;contrastive)).
type_hypothetical(hypothetical):-attr(node,_,abduced,_).
type_hypothetical(alternative):- not type_hypothetical(same), #false:  attr(node,_,abduced,_).
type_hypothetical(same):- #false: attr(node,N,origin,real), not attr(node,N,origin,hypothetical);
                            #false: not attr(node,N,origin,real), attr(node,N,origin,hypothetical).


viz_graph(explanation).
viz_graph(G,explanation):-graph(G).
viz_attr(graph,(real;hypothetical),label,"<<u>{{name}}</u><br/>({{type}})>").
viz_attr(graph,real,(label,name),"Reference").
viz_attr(graph,real,(label,type),"Real").
viz_attr(graph,hypothetical,(label,name),"Found").
viz_attr(graph,hypothetical,(label,type),@stringify(T,true)):-type_hypothetical(T).
viz_attr(graph,contrastive,label,"<<u>Contrastive</u><br/>>"):-graph(contrastive).
viz_attr(graph,G,fontname,"Baskerville"):-graph(G).

% _edge(N,N',(N,N')):- edge(N,N'), not edge(N,N',_).
% _edge(N,N',ID):- edge(N,N',ID).

% ===== Nodes
node(N, contrastive):-node(N).
node(N,G):-node(N),attr(node,N,origin,G).

viz_node((N,G), G):-node(N, G).
viz_attr(node,(N,G),style,filled):-node(N,G).

viz_attr(node,(N,G),fontname,"Baskerville"):-node(N,G).
viz_attr(node,(N,(real;hypothetical)),label,N):-node(N,(real;hypothetical)), not attr(node,N,input,_).
viz_attr(node,(N,real),label,@concat("<<b>",N,"</b>>")):-node(N,real), attr(node,N,input,add).
viz_attr(node,(N,hypothetical),label,@concat("<<b>",N,"</b>>")):-node(N,hypothetical), attr(node,N,input,rm).

viz_attr(node,(N,contrastive),label,N):-node(N,contrastive), not attr(node,N,abduced,_), not attr(node,N, type, c_connector).
viz_attr(node,(N,contrastive),label,@concat("<<s>",N,"</s>>")):-node(N,contrastive), attr(node,N,abduced,rm), not attr(node,N, type, c_connector).
viz_attr(node,(N,contrastive),label,@concat("<<u>",N,"</u>>")):-node(N,contrastive), attr(node,N,abduced,add), not attr(node,N, type, c_connector).

viz_attr(node,(N,real),fillcolor, _color_blue):-node(N, real).
viz_attr(node,(N,hypothetical),fillcolor, _color_green):-node(N, hypothetical).

viz_attr(node,(N,contrastive),fillcolor, @concat(_color_blue,";0.5:",_color_green)):-node(N, hypothetical),node(N, real).
viz_attr(node,(N,contrastive),fillcolor, _color_green):-node(N, hypothetical), not node(N, real).
viz_attr(node,(N,contrastive),fillcolor, @concat(_color_blue,"30")):-not node(N, hypothetical), node(N, real).
viz_attr(node, (N,contrastive), (fontcolor;color), "#11111130") :- not node(N, hypothetical), node(N, real).
% viz_attr(node, (N,contrastive), (fontcolor;color), "#7A1C0360") :- not node(N, hypothetical), node(N, real), attr(node,N,input,rm).
% viz_attr(node, (N,contrastive), (fontcolor;color), "#037A2C60") :- not node(N, hypothetical), node(N, real), attr(node,N,input,add).
% viz_attr(node, (N,contrastive), (fontcolor;color), "#037A2C") :- node(N, hypothetical), node(N, real), attr(node,N,input,add).
% viz_attr(node, (N,real), fontcolor, "#037A2C") :- node(N, real), attr(node,N,input,add).
% viz_attr(node, (N,real), penwidth, 5) :- node(N, real), attr(node,N,input,add).

viz_attr(node, (N,contrastive), penwidth, "5") :- attr(node, N, query, _).

% ===== Edges
viz_edge(((N,contrastive),(N',contrastive),ID), contrastive):-edge(N,N',ID).
viz_edge(((N,G),(N',G),ID),G):-edge(N,N',ID), attr(edge, ID,origin,G).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), style, dashed):-attr(edge,ID,type,inhibitor), edge(N,N',ID).
% viz_attr(edge, ((N,contrastive),(N',contrastive),ID), label, ID):-attr(edge,ID,rule_str,R), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), label, "{{rule}} := [{{vars}}]"):-attr(edge,ID,rule_str,R), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), (label,rule), R):-attr(edge,ID,rule_str,R), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), (label,vars), V):-attr(edge,ID,rule_vars,V), edge(N,N',ID).
% viz_attr(edge, ((N,contrastive),(N',contrastive),(T,(RULE_ID,Vars))), (label,vars), Vars):-edge(N,N',(T,(RULE_ID,Vars))).
% viz_attr(edge, ((N,contrastive),(N',contrastive),ID), (label,vars), ID):-edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), fontsize, 8):-attr(edge,ID,rule_str,R), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), fontcolor, gray):-attr(edge,ID,rule_str,R), edge(N,N',ID).

viz_attr(edge, ((N,contrastive),(N',contrastive),ID), color, _color_blue):-attr(edge,ID,origin,real), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), color, _color_blue):-attr(edge,ID,type,inhibitor), edge(N,N',ID), node(N,real).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), color, _color_green):-attr(edge,ID,origin,hypothetical), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), color, _color_green):-attr(edge,ID,type,inhibitor), edge(N,N',ID), node(N,hypothetical).


%%%%%%%%%%%%%%%%%%%
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), style, dashed) :- attr(edge, ID, type, reciprocal_inhibitor), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), color, red) :-  attr(edge, ID, type, reciprocal_inhibitor), edge(N,N',ID).
viz_attr(edge, ((N,contrastive),(N',contrastive),ID), dir, back) :-  attr(edge, ID, dir, back), edge(N,N',ID).
%%%%%%%%%%%%%%%%%%%

% ==== Handle empty hypothetical

viz_node((invisible, hypothetical), hypothetical):-not node(_, hypothetical).
viz_attr(node,(invisible, hypothetical), label, ""):-not node(_, hypothetical).
viz_attr(node,(invisible, hypothetical), shape, plain):-not node(_, hypothetical).

viz_node((invisible, real), real):-not node(_, real).
viz_attr(node,(invisible, real), label, ""):-not node(_, real).
viz_attr(node,(invisible, real), shape, plain):-not node(_, real).
