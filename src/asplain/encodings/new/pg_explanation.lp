% Selects a single reason for each true atom
% --------------------------------------------
1{  reason((rule(disjunction(H),B),atom(A))):edge((rule(disjunction(H),B),atom(A))), body(B);
    reason((rule(choice(H),B),atom(A))):edge((rule(choice(H),B),atom(A))), body(B)}1      :- hold(A).
