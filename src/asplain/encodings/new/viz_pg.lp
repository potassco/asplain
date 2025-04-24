% Visualizes the program graph using clingraph
% --------------------------------------------------------

#include "reify_defined.lp".

attr(node,N,style,filled):- node(N).

% ## Nodes
attr(node,rule(H,B),shape,box):-node(rule(H,B)).
attr(node,rule(H,B),label,"<<i>{{input}}</i><br/> <b>BODY {{value}}</b> <br/><i>{{output}}</i>>"):-
    node(rule(H,B)).
attr(node,rule(H,normal(B)),(label,value),B):-
    node(rule(H,normal(B))).
attr(node,rule(H,sum(B,G)),(label,value),B):-
    node(rule(H,sum(B,G))).
attr(node,rule(choice(H),B),(label,output),"choice"):-
    node(rule(choice(H),B)).
attr(node,rule(disjunction(H),B),(label,output),"disjuction"):-
    node(rule(disjunction(H),B)).
attr(node,rule(H,normal(B)),(label,input),"normal"):-
    node(rule(H,normal(B))).
attr(node,rule(H,sum(B,G)),(label,input),@concat("sum at least ",G)):-
    node(rule(H,sum(B,G))).

attr(node, atom(A), label, A):- node(atom(A)).

% ## Edges
attr(edge,(A,R),style,dotted):- edge_attr((A,R), type, negative).
attr(edge,(A,R),label,W):- edge_attr((A,R), weight, W).


% ## Highlight model
#const true_color = @color(green,50).
attr(node,rule(H,B),fillcolor,true_color):-node(rule(H,B)), body(B).
attr(node,atom(A),fillcolor,true_color):- node(atom(A)), hold(A).


% ## Highlight explanation
attr(edge,E,color,blue):-reason(E).
