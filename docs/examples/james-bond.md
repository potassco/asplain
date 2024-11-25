If James Bond drinks drug d, he will have paralysis p unless has been
administered an antidote a. The MI5 daily administers Bond antidote a, unless
he is on holiday h. Suppose now that, that day, Bond was actually on a holiday
with Vesper.

```console
asplain encoding.lp --explanation-preference explanation-preference.lp 0
```

![James Bond](../assets/images/james-bond-1.png){width="500"}

=== "encoding.lp"

```prolog
p :- d, not a. %(1)!

a :- not h. %(2)!

d. %(3)!
h.
```

1.  :speech_balloon: Posioned if drinks d and not antidote a. a acts as an inhibitor of p.
2.  :speech_balloon: Antidote if not holiday h inhibitor of a, enabler of p.
3.  :speech_balloon: Bond drinks d and is not on a holiday.

=== "explanation-preference.lp"

```prolog
%===== Abducibles
_abducible((rm;add),d).
_abducible((rm;add),h).

%===== Distance
_distance(Atom, 1, 1) :-
    _abduced(_, Atom).
```

!!! example "James Bond"

    ```
    ... include_encoding(examples/james-bond/encoding.lp){anotations="true"}
    ```

!!! example "James Bond"

    ```
    --8<-- "examples/james-bond/encoding.lp"
    ```

![James Bond](../assets/images/james-bond-1.png){width="500"}
