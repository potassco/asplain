% _abducible((rm;add),d).
% _abducible((rm;add),s).



% ## User input as assumptions
#include "src/asplain/encodings/util_preferences/assumptions_as_input.lp".
_input(h,true).

% ## Distance
% Penalize more abducing something that is not an input
#include "src/asplain/encodings/util_distance/prefer_abduce_input.lp".
