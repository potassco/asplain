#const _color_blue = "#0052CC".
#const _color_purple = "#6554C0".
#const _color_green = "#36B37E".
#const _color_gray = "#B3BAC5".
#const _color_yellow = "#FFAB00".
#const _color_red = "#FF5630".

% ===== Graphs

viz_graph(explanation).
viz_graph(G,explanation):-graph(G).
viz_attr(graph,G,label,@stringify(G,true)):-graph(G).
viz_attr(graph,G,fontname,"Baskerville"):-graph(G).

% ===== Nodes

viz_node((N,G), G):-node(N, G).
viz_attr(node,(N,G),style,filled):-node(N,G).

viz_attr(node,(N,G),fontname,"Baskerville"):-node(N,G).
viz_attr(node,(N,(real;hypothetical)),label,N):-node(N,(real;hypothetical)).

viz_attr(node,(N,contrastive),label,N):-node(N,contrastive), not attr(node,N,abduced,_).
viz_attr(node,(N,contrastive),label,@concat("<<s>",N,"</s>>")):-node(N,contrastive), attr(node,N,abduced,rm).
viz_attr(node,(N,contrastive),label,@concat("<<u>",N,"</u>>")):-node(N,contrastive), attr(node,N,abduced,add).

viz_attr(node,(N,real),fillcolor, _color_blue):-node(N, real).
viz_attr(node,(N,hypothetical),fillcolor, _color_green):-node(N, hypothetical).

viz_attr(node,(N,contrastive),fillcolor, @concat(_color_blue,";0.5:",_color_green)):-node(N, hypothetical),node(N, real).
viz_attr(node,(N,contrastive),fillcolor, _color_green):-node(N, hypothetical), not node(N, real).
viz_attr(node,(N,contrastive),fillcolor, @concat(_color_blue,"30")):-not node(N, hypothetical), node(N, real).
viz_attr(node, (N,contrastive), (fontcolor;color), "#11111130") :- not node(N, hypothetical), node(N, real).
viz_attr(node, (N,contrastive), penwidth, "5") :- attr(node, N, query, _).

% ===== Edges
viz_edge(((N,G),(N',G)),G):-edge((N,N'),G).
viz_attr(edge, ((N,contrastive),(N',contrastive)), style, dashed):-attr(edge,(N,N'),type,inhibitor).

#show node/2.
#show attr/4.
#show edge/2.
#show graph/1.
