# James Bond

If James Bond drinks drug d, he will have paralysis p unless has been
administered an antidote a. The MI5 daily administers Bond antidote a, unless
he is on holiday h. Suppose now that, that day, Bond was actually on a holiday
with Vesper.

## Command line

The command line is used my passing the model where James was poisoned since he
was drudged and was on vacation. We also include the query `p` which means that
we want `p` to be true (James not to be poisoned)

````console
asplain examples/james-bond-choice/encoding.lp  --explanation-preference examples/james-bond-choice/explanation_preference.lp 1 --log info --query "p" --assumptions "-h"```
````
