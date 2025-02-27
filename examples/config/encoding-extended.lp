{ value(X,V) : domain(T,V) } = 1 :- variable(X,T).
% { value(X,V) : domain(T,V) } :- variable(X,T).
% :- value(X, V), value(X, V'), V != V'.
% :- variable(X,T), not value(X,Y): domain(T,Y).
% { value(X,V) : domain(T,V) } :- variable(X,T).

:- constraint(C), not satisfied(C).
satisfied(F) :- binary(F,XL,"=",XR), VL = VR,
                value(XL,VL), value(XR,VR).
satisfied(F) :- binary(F,XL,">",XR), VL > VR,
                value(XL,VL), value(XR,VR).

%NOT WORKING satisfied(F) :- binary(F,XL,"||",XR), 1 <= { satisfied(XL); satisfied(XR) }.
satisfied(F) :- binary(F,XL,"||",XR), satisfied(XL).
satisfied(F) :- binary(F,XL,"||",XR), satisfied(XR).

satisfied(F) :- unary(F,"!",F'), not satisfied(F').
