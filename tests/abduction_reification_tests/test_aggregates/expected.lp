#program base.
% polluted_river.lp
_model(hypothetical,polluted_river(River)) :- not _abduced(rm,polluted_river(River)); _model(hypothetical,river(River)); Sum = #sum { P1: _model(hypothetical,entity(E)), _model(hypothetical,chemical(E,River,P1)); P2: _model(hypothetical,entity(E)), _model(hypothetical,nutrient(E,rhin,P2)) }; Sum > 50.
