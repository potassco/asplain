action(move(B,table)):- block(B).
action(move(B,C)):- block(B),block(C),B!=C.

1 {o(A,T): action(A) } 1 :- step(T).

% position now depends on the previous position
h(on(B),L,T) :- o(move(B,L),T),  h(on(B),L',T-1).
