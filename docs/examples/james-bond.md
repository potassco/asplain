# James Bond

If James Bond drinks drug d, he will have paralysis p unless has been
administered an antidote a. The MI5 daily administers Bond antidote a, unless
he is on holiday h. Suppose now that, that day, Bond was actually on a holiday
with Vesper.

## Command line

The command line is used my passing the model `p. d. h.` where James was poisoned since he was drudged and was on vacation. We also include the query `-p` which means that we want `p` to be false (James not to be poisoned)

```console
asplain examples/james-bond/encoding.lp  --explanation-preference examples/james-bond/explanation-preference.lp 0 --model examples/james-bond/model.lp --query "-p"
```

The computed graphs of the real model (provided) the hypothetical model, as well as the graph contrasting both models.

=== "Explanation 1"
    ![James Bond](../assets/images/james-bond-1.png)
    Shows that `h` had to be removed (crossed out) for the antidote to have been provided so that James is not poisoned.

=== "Explanation 2"
    ![James Bond](../assets/images/james-bond-2.png)
    Shows that `d` had to be removed (crossed out) for James not to be poisoned




## Ecodings

### `encoding.lp`


??? quote "Source code"

    ```prolog
        % If James Bond drinks drug d, he will have paralysis p unless has been administered an antidote a.
        % The MI5 daily administers Bond antidote a, unless he is on holiday h.
        % Suppose now that, that day, Bond was actually on a holiday with Vesper.

        % a inhibitor b: when a is true, b becomes false.
        % a enabler of b: when a is true, b becomes true.

        % Posioned if drinks d and not antidote a.
        %   a acts as an inhibitor of p.
        p :- d, not a.

        % Antidote if not holiday h
        %   h inhibitor of a, enabler of p.
        a :- not h.

        % Bond drinks d and is not on a holiday.
        d.
        h.

        % Only model {d, h, p}
    ```

```prolog
p :- d, not a. %(1)!

a :- not h. %(2)!

d. %(3)!
h.
```

1.  :speech_balloon: Posioned if drinks d and not antidote a. a acts as an inhibitor of p.
2.  :speech_balloon: Antidote if not holiday h inhibitor of a, enabler of p.
3.  :speech_balloon: Bond drinks d and is not on a holiday.

### `explanation-preference.lp`

??? quote "Source code"

    ```prolog
    % Defines the preference for the explanation.

    %===== Abducibles
    %     In this case, atoms `d` and `h` can be either removed or added from the reference model
    %     to find the hypothetical model

    _abducible((rm;add),d).
    _abducible((rm;add),h).

    %===== Distance
    %      It adds a penalty of 1 for each atom that is abduced.

    _distance(Atom, 1, 1) :-
        _abduced(_, Atom).
    ```

Defines the preference for the explanation.


=== "Abducibles"

    In this case, atoms `d` and `h` can be either removed or added from the reference model
    to find the hypothetical model

    ```prolog
    _abducible((rm;add),d).
    _abducible((rm;add),h).
    ```

=== "Distance"

    It adds a penalty of 1 for each atom that is abduced.

    ```prolog
    _distance(Atom, 1, 1) :-
        _abduced(_, Atom).
    ```


<!--
!!! example "James Bond"

    ```
    ... include_encoding(examples/james-bond/encoding.lp){anotations="true"}
    ```

!!! example "James Bond"

    ```
    --8<-- "examples/james-bond/encoding.lp"
    ```

![James Bond](../assets/images/james-bond-1.png){width="500"} -->
