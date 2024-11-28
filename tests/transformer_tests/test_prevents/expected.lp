#program base.
% sentence(P,innocent) :- person(P); not punish(P).
_sup(1,World,sentence(P,innocent),(P,)) :- world(World); _model(World,person(P)); not _model(World,punish(P)).
_depends(_sup(1,World,sentence(P,innocent),(P,)),person(P)) :- _sup(1,World,sentence(P,innocent),(P,)).
_prevents(_sup(1,World,sentence(P,innocent),(P,)),punish(P)) :- _sup(1,World,sentence(P,innocent),(P,)).