% Used to enforce a model that might be given

#defined _model/1. %Comes from the input
:- hold(atom(A)), not _model(A).
:- not hold(atom(A)), _model(A).
