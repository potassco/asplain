
% Make all fact facts abducible
% node_tag(rule(H,B),abducible(rm)):-node_tag(rule(H,B),fact), edge((rule(H,B), atom(A))).
% Make only alcohol and drive abducible
node_tag(rule(H,B),abducible(rm)):-node_tag(rule(H,B),fact), edge((rule(H,B), atom(drive(P)))).
node_tag(rule(H,B),abducible(rm)):-node_tag(rule(H,B),fact), edge((rule(H,B), atom(alcohol(P)))).

% Allow including any disabled rule
% !!!! Tricky since we use disabled for the abducible we need to check if it was disabled in the reference not in the current
node_tag(rule(H,B),abducible(add)):-node_tag(rule(H,B),disabled,reference).


#include "src/asplain/encodings/util_distance/abduce_the_least.lp".
