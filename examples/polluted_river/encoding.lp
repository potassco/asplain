% polluted_river.lp

river(rin).
factory(a).
factory(b).
farm(c).

chemical(a, rin, 15).
chemical(b, rin, 30).
chemical(c, rin, 2).
nutrient(c, rin, 20).

entity(E, factory) :- factory(E).
entity(E, farm) :- farm(E).

polluted_river(River) :-
    river(River),
    #sum{
        P1, E: entity(E, T), chemical(E, River, P1);
        P2, E: entity(E, T), nutrient(E, rin, P2)}>25.
