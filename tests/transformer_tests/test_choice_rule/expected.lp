#program base.
% 1 <= { o(A,T): action(A); special_o(A,T): special_action(A) } <= 1 :- step(T).
_sup(1,World,o(A,T),(T,)) :- world(World); _model(World,step(T)).
_depends(_sup(1,World,o(A,T),(T,)),(step(T);action(A))) :- _sup(1,World,o(A,T),(T,)).
_sup(2,World,special_o(A,T),(T,)) :- world(World); _model(World,step(T)).
_depends(_sup(2,World,special_o(A,T),(T,)),(step(T);special_action(A))) :- _sup(2,World,special_o(A,T),(T,)).
