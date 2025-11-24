% Defines the preference for the explanation.

%===== Abducibles
%     In this case, atoms `d` and `h` can be either removed or added from the reference model
%     to find the hypothetical model

node_tag(R, abducible(rm,d)):- node_tag(R,fact),  edge(R,atom(d)).

% #include "src/asplain/encodings/util_preferences/abducible_constraints_single.lp".

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

% Abduce the least rules
#include "src/asplain/encodings/util_distance/abduce_the_least.lp".
#include "src/asplain/encodings/util_distance/prefer_abduce_assumptions.lp".
