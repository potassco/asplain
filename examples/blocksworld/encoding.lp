% time(0..last). step(1..last). block(1..n).
time(0..Last) :- last(Last).
step(1..Last) :- last(Last).
block(1..N) :- n(N).
location(table). location(B):-block(B).

unclear(C,T) :- h(on(B),C,T),C!=table,time(T).
:- o(move(B,_),T), unclear(B,T-1).                   % cannot move a block with has another on top of it
:- o(move(_,L),T), unclear(L,T-1).                   % cannot move a block onto another that is not on top of a tower
:- o(move(B,table),T), h(on(B),table,T-1), step(T).  % cannot move a block from the table to another place in the table
:- g(on(B),L), not h(on(B),L,Last), last(Last).      % reach goal

h(F,V,T) :- h(F,V,T-1), not c(F,T), step(T).         % inertia
c(F,T)   :- h(F,V,T-1),h(F,W,T),V!=W, step(T).       % changes

#show h/3.
