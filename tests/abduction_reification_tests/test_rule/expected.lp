#program base.
_model(hypothetical,punish(P)) :- not _abduced(rm,punish(P)); _model(hypothetical,drive(P)); _model(hypothetical,alcohol(P)); _model(hypothetical,person(P)).
_model(hypothetical,punish(P)) :- not _abduced(rm,punish(P)); _model(hypothetical,resist(P)); _model(hypothetical,person(P)).
_model(hypothetical,sentence(P,prison)) :- not _abduced(rm,sentence(P,prison)); _model(hypothetical,punish(P)).
_model(hypothetical,sentence(P,innocent)) :- not _abduced(rm,sentence(P,innocent)); _model(hypothetical,person(P)); not _model(hypothetical,punish(P)).