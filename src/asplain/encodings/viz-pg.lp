#script (python)
from clingo import Number
ids = {}
def rule_id(rule):
    if str(rule) in ids:
        n= ids[str(rule)]
    else:
        id = len(ids) + 1
        ids[str(rule)] = id
        n = id
    return Number(n)
#end.

% Settings
#external show(reference).
#external show(foil).
#external show(contrastive).
#external show(model(reference)).
#external show(model(foil)).

#const _color_blue = "#0052CC50".
#const _color_green = "#36B37E".
#const _color_orange = "#FFAB0050".
#const _color_red = "#FF5630".
#const _color_gray = "#B3BAC550".
#const _color_light = "#B3BAC560".
#const _color_purple = "#6554C0".
#const _color_both = "#57B5BD50".
color_set(model(reference), @concat(_color_purple,"80")):-not show(model(foil)).
color_set(model(reference), @concat(_color_purple,"25")):-show(model(foil)).
color_set(model(foil), _color_green).
color_set(union, "#36B37E;0.5:#6554C080").
color_set(constraint, @concat(_color_red,"25")).
color_set(light, gray84).

#const setdpi = 80.

vnode(X):-node(G, X), show(G).
vedge((X,Y)):-edge(G, _,(X, Y)), show(G), vnode(X), vnode(Y).
vtag(X,T):-tag(G, X, T), show(G).

vattr(graph,default,label,"<<b>{{name}}</b><br/>{{description}}>"):-show_title.
vattr(graph,default,(label,name),T):-title(T),show_title.
vattr(graph,default,bgcolor,"#00000000").
vattr(graph,default,dpi,setdpi).

% Rule labels
vattr(node,rule(H,B),label,"<<font point-size=\"9\"> </font><br/> r{{value}} <br/> <u><font point-size=\"9\"><i>{{output}}</i></font></u>>"):-
    vnode(rule(H,B)).
vattr(node,rule(choice(H),B),(label,output),"choice"):-
    vnode(rule(choice(H),B)).
vattr(node,rule(disjunction(H),B),(label,output),"disjunction"):-
    vnode(rule(disjunction(H),B)).

% WARNING this just works with a single file and being already grounded, otherwise you get repeated ids
vattr(node,rule(H,B),(label,value),ID):-
    vnode(rule(H,B)), tag(_, rule(H,B), rule_id(ID)).
% vattr(node,rule(H,B),(label,value),@rule_id(rule(H,B))):-
%     vnode(rule(H,B)).

% Atom labels
vattr(node, atom(A), label, "< <font point-size=\"12\">{{atom}}</font> >"):- vnode(atom(A)).
vattr(node, atom(A), (label,atom), A):- vnode(atom(A)).

% General style
vattr(node,N,fontname,@clinguin_fontname()):-  vnode(N).

% Rule style
vattr(node,rule(H,B),shape,box):-vnode(rule(H,B)).
vattr(node,N,style,filled):- vnode(N), not abducible(_, N).
vattr(node,N,style,"filled,dashed"):- vnode(N), abducible(_, N).

% Tooltips
vattr(node,N,tooltip,"<{{rule}}    {{label}}>"):- vnode(N), vtag( N, rule_fo(S)).
vattr(node,N,(tooltip,rule),S):- vnode(N), vtag( N, rule_fo(S)).
vattr(node,N,(tooltip,label),S):- vnode(N), vtag( N, label(S)).
vattr(node,atom(A),tooltip,S):- vnode(atom(A)), vtag( atom(A), label(S)).

% Colors
no_model(N):- vnode(N), show(model(_)), not node(model(G), N):show(model(G)).
both_models(N):- vnode(N), show(model(reference)), show(model(foil)), node(model(reference), N), node(model(foil), N).
vattr(node,N,fillcolor,white):- vnode(N), not show(model(_)), not red_node(N).
vattr(node,N,fillcolor,C):- not both_models(N), vnode(N), show(model(G)), node(model(G), N), color_set(model(G),C).
vattr(node,N,fillcolor,C):- both_models(N), color_set(union,C).
vattr(node,N,fillcolor,white):- vnode(N), no_model(N), not red_node(N).

highlighted_model(foil):- show(model(foil)).
highlighted_model(reference):- show(model(reference)), not show(model(foil)).

active_node(N):- vnode(N), highlighted_model(M), node(model(M), N).
active_node(N):- vnode(N), not show(model(_)), node(reference, N), not show(foil).
active_node(N):- vnode(N), not show(model(_)), node(foil, N).

gray_node(N):-vnode(N),
            not active_node(N),
            not abduced(_,N).
vattr(node,N,(fontcolor;color),C):- gray_node(N),
                                color_set(light,C).
abduced(rm,R):-node(reference, R), not node(foil, R), show(foil).
abduced(add,R):-node(foil, R), not node(reference, R), show(foil).
vattr(node,R,(fontcolor;color),red):- abduced(rm,R).
vattr(node,R,(fontcolor;color),blue):- abduced(add,R).

% -------------- Edges
vattr(edge,(A,R),style,dashed):- edge(_, negative,(A,R)).
vattr(edge,E,arrowhead,vee):- vedge(E).
vattr(edge,E,arrowsize,"0.5"):- vedge(E).

active_edge(E):- vedge(E), highlighted_model(M), edge(model(M),T, E).
active_edge(E):- vedge(E), not show(model(_)), edge(reference,T, E), not show(foil).
active_edge(E):- vedge(E), not show(model(_)), edge(foil,T, E).
vattr(edge,((N1),(N2)),color,C):-vedge((N1,N2)), not active_edge(((N1),(N2))), color_set(light,C).


red_node(X):-node(contrastive, X), tag(_, X, constraint).
vattr(node,X, fillcolor, C):-red_node(X), color_set(constraint,C).
