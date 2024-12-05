unclear(C,T) :- h(on(B),C,T),C!=table,time(T).
:- o(move(B,_),T), unclear(B,T-1).                   % executability
:- o(move(_,L),T), unclear(L,T-1).                   % executability
:- o(move(B,table),T), h(on(B),table,T-1), step(T).  % executability
:- g(on(B),L), not h(on(B),L,last).
