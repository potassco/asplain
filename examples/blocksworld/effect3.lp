action(move(B,table)):- block(B).
action(move(B,C)):- block(B),block(C),B!=C.

% moves depend on the previous position
1{o(A,T): action(A), A=move(B,L), on((B),L',T-1)}1 :- step(T).
h(on(B),L,T) :- o(move(B,L),T).
