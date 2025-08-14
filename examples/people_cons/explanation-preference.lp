% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

% _abducible((rm;add),sit(P)):-node(atom( person(P))).
% _abducible((rm;add),stand(P)):-node(atom( person(P))).
% _abducible((rm;add),age(P,E)):-node(atom( age(P,E))).

node_tag(rule(H,B),abducible(rm)):-node_tag(rule(H,B),fact), edge((rule(H,B), atom(age(P,E)))).


%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

distance(Atom, 1, 2) :-
    abduced(_, Atom).

% _direct_inhibitor(2, real, sit, stand).
% _direct_inhibitor(2, hypothetical, stand, sit).


% ## reduce
% This is tricky to write since one holds in holds/2 and one is holds/1
distance(Atom, 1, 1) :-
    used_to_hold(Atom), not hold(Atom).

distance(Atom, 1, 1) :-
    not used_to_hold(Atom), hold(Atom).

distance(Reason, 1, 1) :-
    reason(Reason,reference), not reason(Reason).
