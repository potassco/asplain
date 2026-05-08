tag(R, removable):-
    A = initial(X,Y,V),
    node(A, atom),
    tag(R, fact),
    edge((R,A),1).
