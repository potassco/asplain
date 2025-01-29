#program base.
_model(hypothetical,person(X)) :- not _abduced(rm,person(X)); _model(hypothetical,parent(X,_Annon_1)).
_model(hypothetical,person(X)) :- not _abduced(rm,person(X)); _model(hypothetical,parent(_Annon_2,X)).
