#program base.
% 1 <= { o(A,T): action(A); special_o(A,T): special_action(A) } <= 1 :- step(T).
_rule(1,"1 <= { o(A,T): action(A); special_o(A,T): special_action(A) } <= 1 :- step(T).").
_sup(1,World,o(A,T),(A,T)) :- world(World); _model(World,step(T)); _model(World,action(A)).
_depends(_sup(1,World,o(A,T),(A,T)),(step(T);action(A))) :- _sup(1,World,o(A,T),(A,T)).
_sup(1,World,special_o(A,T),(A,T)) :- world(World); _model(World,step(T)); _model(World,special_action(A)).
_depends(_sup(1,World,special_o(A,T),(A,T)),(step(T);special_action(A))) :- _sup(1,World,special_o(A,T),(A,T)).
_rule(2,"#false :- 1 < #count { o(A,T): o(A,T), action(A); special_o(A,T): special_o(A,T), special_action(A) }; step(T).").
_sup_constraint(2,(T,)) :- world(World); 1 < #count { o(A,T): _model(_,o(A,T)), _model(_,action(A)); special_o(A,T): _model(_,special_o(A,T)), _model(_,special_action(A)) }; _model(_,step(T)).
_constraints(_sup_constraint(2,(T,)),step(T)) :- _sup_constraint(2,(T,)).
_constraints(_sup_constraint(2,(T,)),(o(A,T);action(A))) :- _model(_,o(A,T)); _model(_,action(A)); _sup_constraint(2,(T,)).
_constraints(_sup_constraint(2,(T,)),(special_o(A,T);special_action(A))) :- _model(_,special_o(A,T)); _model(_,special_action(A)); _sup_constraint(2,(T,)).
_rule(3,"#false :- 1 > #count { o(A,T): o(A,T), action(A); special_o(A,T): special_o(A,T), special_action(A) }; step(T).").
_sup_constraint(3,(T,)) :- world(World); 1 > #count { o(A,T): _model(_,o(A,T)), _model(_,action(A)); special_o(A,T): _model(_,special_o(A,T)), _model(_,special_action(A)) }; _model(_,step(T)).
_constraints(_sup_constraint(3,(T,)),step(T)) :- _sup_constraint(3,(T,)).
_constraints(_sup_constraint(3,(T,)),(o(A,T);action(A))) :- _model(_,o(A,T)); _model(_,action(A)); _sup_constraint(3,(T,)).
_constraints(_sup_constraint(3,(T,)),(special_o(A,T);special_action(A))) :- _model(_,special_o(A,T)); _model(_,special_action(A)); _sup_constraint(3,(T,)).