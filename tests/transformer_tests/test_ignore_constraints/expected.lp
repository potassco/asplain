#program base.
% unclear(C,T) :- h(on(B),C,T); C != table; time(T).
_sup(1,World,unclear(C,T),(B,C,T)) :- world(World); _model(World,h(on(B),C,T)); C != table; _model(World,time(T)).
_depends(_sup(1,World,unclear(C,T),(B,C,T)),(h(on(B),C,T);time(T))) :- _sup(1,World,unclear(C,T),(B,C,T)).
% #false :- o(move(B,_),T); unclear(B,(T-1)).
% executability
% #false :- o(move(_,L),T); unclear(L,(T-1)).
% executability
% #false :- o(move(B,table),T); h(on(B),table,(T-1)); step(T).
% executability  
% #false :- g(on(B),L); not h(on(B),L,last).