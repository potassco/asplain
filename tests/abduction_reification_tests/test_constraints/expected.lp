#program base.
:- _model(hypothetical,assign(P,S)); _model(hypothetical,assign(P',S)); _model(hypothetical,P' > P).
:- _model(hypothetical,assign(P,(T,C))); _model(hypothetical,assign(P',(T,C'))); _model(hypothetical,person(P,cat)); _model(hypothetical,person(P',dog)).