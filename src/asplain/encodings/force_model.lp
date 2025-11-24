% Used to enforce a model that might be given

#defined _force_model/0. %Comes from the input
#defined _model/1. %Comes from the input
:- hold(A), not _model(A), _force_model.
:- not hold(A), _model(A), _force_model.
