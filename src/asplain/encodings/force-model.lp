% Used to enforce a model that might be given

#defined model/1. %Comes from the input
:- hold(atom(A)), not model(A).
:- not hold(atom(A)), model(A).
