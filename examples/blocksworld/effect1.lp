% actions, moves and positions do not depend on the previous state

action(move(B,table)):- block(B).
action(move(B,C)):- block(B), block(C), B!=C.

1 {o(A,T): action(A) } 1 :- step(T).
h(on(B),L,T) :- o(move(B,L),T).
