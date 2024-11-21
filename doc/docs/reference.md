---
icon: material/bookmark-multiple
---

# Reference


## Encodings

Here are the used encodings

### Visualization with *clingraph*

```prolog
%%%%%%%%%%%%%% xclingo_show_contrastive.lp %%%%%%%%%%%%%%%%%

% 1. Shows only the atoms that are part of the contrastive graph.
% 2. Shows the style atoms for clingrpah.

#const _color_blue = "#0052CC".
#const _color_purple = "#6554C0".
#const _color_green = "#36B37E".
#const _color_gray = "#B3BAC5".
#const _color_yellow = "#FFAB00".
#const _color_red = "#FF5630".


graph(contrastive).
% Nodes of the contrastive
node(Atom, Graph) :- _xclingo_node(Atom, Graph), Graph=contrastive.

% Edges of the contrastive
edge((Caused, Cause), Graph) :- _xclingo_edge((Caused, Cause), Graph), Graph=contrastive.

% Labels
attr(node, Atom, label, "<<s>{{l}}</s>>") :- _xclingo_attr(node, Atom, label, Label), _xclingo_node(Atom, contrastive),_xclingo_abduced(rm, Atom).
attr(node, Atom, (label,l), Label) :- _xclingo_attr(node, Atom, label, Label), _xclingo_node(Atom, contrastive).
% #show attr(node, Atom, label, Label) : attr(node, Atom, label, Label), _xclingo_node(Atom, contrastive),not _xclingo_abduced(rm, Atom).

%%% General attributes
attr(node, Atom, style, filled) :- _xclingo_f_atom(_, Atom).
attr(node, Atom, fillcolor, "{{color}}{{opacity}}") :- _xclingo_f_atom(_, Atom).
attr(node,Atom,fontname,"Baskerville"):- _xclingo_f_atom(_, Atom).

% green: only hypothetical
attr(node, Atom, (fillcolor,color), _color_green) :- _xclingo_f_atom(hypothetical, Atom), not _xclingo_f_atom(real, Atom).
% blue: real
attr(node, Atom, (fillcolor,color), _color_blue) :- _xclingo_f_atom(real, Atom).
% Opaque only real (not in hypothetical)
attr(node, Atom, (fillcolor,opacity), "30") :-
     _xclingo_f_atom(real, Atom), not _xclingo_f_atom(hypothetical, Atom).
attr(node, Atom, (fontcolor;color), "#11111130") :-
    _xclingo_f_atom(real, Atom), not _xclingo_f_atom(hypothetical, Atom).

%%% edge style
attr(edge, (Caused, Cause), style, dashed) :-
    edge((Caused, Cause), contrastive),
    _xclingo_f_atom(hypothetical, Caused), not _xclingo_f_atom(real, Caused),
    _xclingo_f_atom(real, Cause), not _xclingo_f_atom(hypothetical, Cause).

attr(edge, (Caused, Cause), color,  "#11111130") :-
    edge((Caused, Cause), contrastive),
    _xclingo_f_atom(real, Cause), not _xclingo_f_atom(hypothetical, Cause).

% Bottom to Top
attr(graph, Graph, rankdir, "BT") :- _xclingo_graph(Graph).
% Directed graph (now its 'backwards' because the encoding is in the opposite direction)
attr(edge, (Caused, Cause), dir, back) :- edge((Caused, Cause), Graph).


#show node/2.
#show attr/4.
#show edge/2.
#show graph/1.

```

## API
