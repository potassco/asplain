#program base.
% polluted_river.lp
% polluted_river(River) :- river(River); Sum = #sum { P1: entity(E), chemical(E,River,P1); P2: entity(E), nutrient(E,rhin,P2) }; Sum > 50.
_rule(1,"polluted_river(River) :- river(River); Sum = #sum { P1: entity(E), chemical(E,River,P1); P2: entity(E), nutrient(E,rhin,P2) }; Sum > 50.").
_sup(1,World,polluted_river(River),(River,Sum)) :- world(World); _model(World,river(River)); Sum = #sum { P1: _model(World,entity(E)), _model(World,chemical(E,River,P1)); P2: _model(World,entity(E)), _model(World,nutrient(E,rhin,P2)) }; Sum > 50.
_depends(_sup(1,World,polluted_river(River),(River,Sum)),river(River)) :- _sup(1,World,polluted_river(River),(River,Sum)).
_depends(_sup(1,World,polluted_river(River),(River,Sum)),(entity(E);chemical(E,River,P1))) :- _model(World,entity(E)); _model(World,chemical(E,River,P1)); _sup(1,World,polluted_river(River),(River,Sum)).
_depends(_sup(1,World,polluted_river(River),(River,Sum)),(entity(E);nutrient(E,rhin,P2))) :- _model(World,entity(E)); _model(World,nutrient(E,rhin,P2)); _sup(1,World,polluted_river(River),(River,Sum)).