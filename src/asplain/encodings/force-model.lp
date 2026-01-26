% Used to enforce a model that might be given

#defined model/1. %Comes from the input
:- hold(A), not model(A), node_type(A, atom).
:- not hold(A), model(A), node_type(A, atom).
