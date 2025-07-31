
_abducible(rm, chemical(Entity, River, Pollution)) :- _model(real, chemical(Entity, River, Pollution)).
_abducible(rm, nutrient(Entity, River, Pollution)) :- _model(real, nutrient(Entity, River, Pollution)).

% Default distance
distance(Atom, 0, 1) :- abduced(_, Atom).

% Distance based on the amount of pollution removed
any_rmved_pollution(Atom, Pollution) :-
    abduced(rm, Atom), Atom = nutrient(Entity, Atom, Pollution).

any_rmved_pollution(Atom, Pollution) :-
    abduced(rm, Atom), Atom = chemical(Entity, Atom, Pollution).

distance(Atom, NPollution, 2) :- any_rmved_pollution(Atom, NPollution).
