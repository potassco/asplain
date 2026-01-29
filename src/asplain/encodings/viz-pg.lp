% Settings
% #external show(reference).
% #external show(foil).
% #external show(contrastive).
% #external show(model(reference)).
% #external show(model(foil)).
world(ref;foil).

#const _color_blue = "#0052CC50".
#const _color_green = "#36B37E".
#const _color_orange = "#FFAB0050".
#const _color_red = "#FF5630".
#const _color_gray = "#B3BAC550".
#const _color_light = "#B3BAC560".
#const _color_purple = "#6554C0".
#const _color_both = "#57B5BD50".
% color_set(model(reference), @concat(_color_purple,"80")):-not show(model(foil)).
color_set(ref, @concat(_color_purple,"25")):- solved(foil).
color_set(ref, @concat(_color_purple,"80")):- not solved(foil).
color_set(foil, _color_green).
color_set(union, "#36B37E;0.5:#6554C080").
color_set(constraint, @concat(_color_red,"25")).
color_set(light, gray84).

#const setdpi = 80.

vnode(X):-node(X,_),solved(foil),     program(X, foil).
vnode(X):-node(X,_),solved(foil), not program(X, foil),     program(X, ref).
vnode(X):-node(X,_),not solved(foil), solved(ref), program(X, ref).
vnode(X):-node(X,_),not solved(foil), not solved(ref).
vedge((X,Y)):-edge((X, Y),_), vnode(X), vnode(Y).
vtag(X,T):-tag(X, T).

vattr(graph,default,label,"<<b>{{name}}</b><br/>{{description}}>"):-show_title.
vattr(graph,default,(label,name),T):-title(T),show_title.
vattr(graph,default,bgcolor,"#00000000").
vattr(graph,default,dpi,setdpi).

% Rule labels
vattr(node,R,label,"<<font point-size=\"8\"> </font><br/> r{{value}} <br/> <u><font point-size=\"9\"><i>{{output}}</i></font></u>>"):-
    vnode(R), node(R,rule(_)).
vattr(node,R,(label,output),"choice"):-
    vnode(R), node(R,rule(choice)).
vattr(node,R,(label,output),"disjunction"):-
    vnode(R), node(R,rule(disjunction)).
vattr(node,R,(label,value),R):-
    vnode(R).

% Atom labels
vattr(node, A, label, "< <font point-size=\"10\">{{value}}</font> >"):- vnode(A), node(A, atom).

% General style
vattr(node,N,fontname,@clinguin_fontname()):-  vnode(N).

% Rule style
vattr(node,N,shape,box):-vnode(N), node(N,rule(_)).
vattr(node,N,style,filled):- vnode(N).
% vattr(node,N,style,filled):- vnode(N), not abducible(_, N).
% vattr(node,N,style,"filled,dashed"):- vnode(N), abducible(_, N).

% Tooltips
vattr(node,N,tooltip,"<{{rule}}    {{label}}>"):- vnode(N).
vattr(node,N,(tooltip,rule),@html_escape(S)):- vnode(N), vtag( N, rule_fo(S)).
vattr(node,N,(tooltip,label),@html_escape(S)):- vnode(N), vtag( N, label(S)).

% Colors
no_model(N):- vnode(N), not model(N, ref), not model(N, foil).
both_models(N):- vnode(N), model(N, ref), model(N, foil).
vattr(node,N,fillcolor,C):- vnode(N), not both_models(N), model(N,G), color_set(G,C).
vattr(node,N,fillcolor,C):- both_models(N), color_set(union,C).
vattr(node,N,fillcolor,white):- vnode(N), no_model(N), not fired(N).
% vattr(node,N,fillcolor,white):- vnode(N).


active_node(N):- vnode(N), node(N,_), not solved(foil).
active_node(N):- vnode(N), node(N,_), model(N, foil), solved(foil).
% active_node(N):- vnode(N), not show(model(_)), node(ref, N), not show(foil).
% active_node(N):- vnode(N), not show(model(_)), node(foil, N).

abduced(rm,R):-node(R,_), program(R, ref), not program(R, foil), solved(foil).
abduced(add,R):-node(R,_), program(R, foil), not program(R, ref), solved(foil).

gray_node(N):-vnode(N),
            not active_node(N),
            not abduced(_,N).

vattr(node,N,(fontcolor;color),C):- gray_node(N),
                                color_set(light,C).
vattr(node,R,(fontcolor;color),red):- abduced(rm,R).
vattr(node,R,(fontcolor;color),blue):- abduced(add,R).

% -------------- Edges
vattr(edge,E,style,dashed):- vedge(E), edge(E,0).
vattr(edge,E,arrowhead,vee):- vedge(E).
vattr(edge,E,arrowsize,"0.5"):- vedge(E).

active_edge((N1,N2)):- vedge((N1,N2)), active_node(N1), active_node(N2).
vattr(edge,E,color,C):- vedge(E), not active_edge(E), color_set(light,C).


vattr(node,X, fillcolor, C):-fired(X), color_set(constraint,C).
