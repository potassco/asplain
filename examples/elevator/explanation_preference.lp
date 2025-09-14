% Make only called abducible
node_tag(rule(H,B),abducible(rm)):-node_tag(rule(H,B),fact), edge((rule(H,B), atom(called(P1,P2)))).

#include "src/asplain/encodings/util_distance/abduce_the_least.lp".
