change(rm,N)  :- node(N,_), program(N, ref), not program(N, foil), solved(foil).
change(add,N) :- node(N,_), program(N, foil), not program(N, ref), solved(foil).
