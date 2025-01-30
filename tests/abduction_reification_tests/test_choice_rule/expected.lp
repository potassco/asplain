#program base.
1 <= { _model(hypothetical,o(A,T)): not _abduced(rm,o(A,T)), _model(hypothetical,action(A)); _model(hypothetical,special_o(A,T)): not _abduced(rm,special_o(A,T)), _model(hypothetical,special_action(A)) } <= 1 :- _model(hypothetical,step(T)).
