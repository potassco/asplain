% Used to enforce a model that might be given

#defined model/1. %Comes from the input
:- model(A,ref), not model(A), node_type(A, atom).
:- not model(A,ref), model(A), node_type(A, atom).
