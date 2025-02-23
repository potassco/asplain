
1{o(move(B,From,To),T): location(To),To!=B, h(on(B),From,T-1)}1 :- step(T).
o(move(B,To),T) :- o(move(B,From,To),T).

h(on(B),L,T) :- o(move(B,L),T).
