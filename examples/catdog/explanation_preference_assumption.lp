% #include "src/asplain/encodings/util_preferences/abducible_constraints_single.lp".

%===== Distance
%      It adds a penalty of 1 for each atom that is abduced.

% Abduce the least rules
#include "src/asplain/encodings/util_distance/abduce_the_least.lp".
#include "src/asplain/encodings/util_distance/prefer_abduce_assumptions.lp".
