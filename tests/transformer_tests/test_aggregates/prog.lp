% polluted_river.lp
polluted_river(River) :- 
    river(River),
    #sum{P1: entity(E), chemical(E, River, P1); P2: entity(E), nutrient(E, rhin, P2)}=Sum, 
    Sum>50.
