
% Create the union and the extra nodes

node(contrastive, X):-node(model(_), X).
edge(contrastive, S, (X,Y)):-edge(model(_), S, (X,Y)), node(contrastive,X), node(contrastive,Y).

true_lit((atom(A), rule(H,B))):- node(contrastive,atom(A)), edge(_,positive, (atom(A), rule(H,B))).
true_lit((atom(A), rule(H,B))):- node(contrastive,atom(A)), not node(model(foil),atom(A)), edge(_,negative, (atom(A), rule(H,B))).
true_lit((atom(A), rule(H,B))):- node(contrastive,atom(A)), not node(model(reference),atom(A)), edge(_,negative, (atom(A), rule(H,B))).
node(contrastive, rule(H,B)):-
    tag(_, rule(H,B), constraint),
    true_lit((atom(A),rule(H,B))): edge(_,S,(atom(A),rule(H,B))).

% TODO maybe we could add a tag here to improve the LLM
