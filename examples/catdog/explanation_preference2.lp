%%% _abducible(A)
% A is an abducible atom
% If A is true in the model then it may be removed for the contrastive explanation.
% If A is false in the model then it may be added for the contrastive explanation

_abducible((rm;add),assign(P,S)):-_model(real, person(P,_)),_model(real, seat(S)).

_distance(Atom, 1, 1) :-
    _abduced(_, Atom).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
reciprocal_inhibitor(C, Vars,  A1, A2) :-
    _fired_constraint((C, Vars), A1), _fired_constraint((C, Vars), A2), A1!=A2.

% _constraints(C_Id) :- _fired_constraint(C_Id, _, _).

% _diff_activations((C, Vars1), (C, Vars2)) :-
%     _fired_constraint((C, Vars1), A1),          % We take a fired constraint (C, Vars1) and an atom A1 from it
%     _constraints((C, Vars2)), Vars1 != Vars2,   % We take a second fired constraint (C, Vars2) of the same constraint, different activation
%     not _fired_constraint((C, Vars2), A1).      % Such that A1 is not in (C, Vars2) (there is a difference)

% _symm_activations((C, Vars1), (C, Vars2)) :-
%     _constraints((C, Vars1)), _constraints(C, Vars2),
%     not _diff_activations((C, Vars1), (C, Vars2)).

% selected_constraint(C) :- _constraints(C), not _symm_activations(C, _).
% aux(C) :-
%     _constraints(C),
%     _symm_activations(C, C2),
%     C < C2,
%     not selected_constraint(C2).
% selected_constraint(C) :- _constraints(C), not aux(C).


% % :- person(P,A), assign(P, S), assign(P', S), P' != P.
% _fired_constraint(c2, (P,A,P',S), (person(P,A); assign(P', S); assign(P, S)), "Different persons in the same seat.") :-
%     _model(_, person(P, A)), _model(_, assign(P, S)), _model(_, assign(P', S)), P' != P.

% % :- person(P,A), assign(P, S), assign(P', S), P' != P.
% _constraint_meessage(c3, "Different persons in the same seat.").
% _fired_constraint((c3, (P,A,P',S)), (person(P,A); assign(P', S); assign(P, S))) :-
%     _model(_, person(P, A)), _model(_, assign(P, S)), _model(_, assign(P', S)), P' != P.

% % :- assign(P,S), assign(P',S), P'>P.
_constraint_meessage(c4, "Same seat, different person.").


_fired_constraint((c4, (P,S,P')), (assign(P', S); assign(P, S))) :-
    _model(_, assign(P, S)), _model(_, assign(P', S)), P' > P.

% :- assign(P,(T,C)), assign(P',(T,C')), person(P,cat), person(P',dog).
_constraint_meessage(c5, "Two Cat or Dog people in the same Table.").
_fired_constraint((c5, (P,T,C,P',C')), (assign(P,(T,C)); assign(P',(T,C')); person(P,cat); person(P',dog))) :-
    _model(_, assign(P, (T,C))),
    _model(_, assign(P', (T,C'))),
    _model(_, person(P, cat)),
    _model(_, person(P', dog)).
