{ value(X,V) : domain(T,V) } = 1 :- variable(X,T).

:- value(X,V1), value(X,V2), V1 != V2.
:- constraint(C), not satisfied(C).
satisfied(F) :- binary(F,XL,"=",XR), VL = VR,
                value(XL,VL), value(XR,VR).

#show value/2.
