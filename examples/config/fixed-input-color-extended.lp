% _input(value("color","Red")).
% _input(add,value("frontWheel",18)).
% _input(add,value("rearWheel",18)).
% :- not _model(hypothetical,value("rearWheel",18)), not _abduced(rm, value("rearWheel",18)).
:- not _model(hypothetical,value("rearWheel",18)).
