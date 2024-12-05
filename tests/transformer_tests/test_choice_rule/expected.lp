#program base.
% 1 <= { o(A,T): action(A); special_o(A,T): special_action(A) } <= 1 :- step(T).
_sup(1,World,o(A,T),(A,T)) :- world(World); _model(World,step(T)); _model(World,action(A)).
_depends(_sup(1,World,o(A,T),(A,T)),(step(T);action(A))) :- _sup(1,World,o(A,T),(A,T)).
_sup(2,World,special_o(A,T),(A,T)) :- world(World); _model(World,step(T)); _model(World,special_action(A)).
_depends(_sup(2,World,special_o(A,T),(A,T)),(step(T);special_action(A))) :- _sup(2,World,special_o(A,T),(A,T)).
