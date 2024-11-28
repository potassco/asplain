# Solving


## `base.lp`


??? quote "Source code"

    ```prolog
    #include "abduction.lp".
    #include "contrastive.lp".
    #include "graphs.lp".

    % #show _direct_cause/4.
    % #show _direct_inhibitor/4.
    % #show _query/2.
    % #show _abduced/2.
    #show node/1.
    #show edge/2.
    #show attr/4.
    ```

Computes the contrastive graphs using abduction.

**Input predicates:**

| Name           | Description       |
| :------------- | :----------------- |
| `_model(real,A)`    | Atom `A` is part of the real (reference) model |
| `_distance(N,D,L)`    | A penalization with id `N` is added of value `D` at level `L` (larger levels are more important) |
| `_abducible(T,A)`    | Atom `A` can be removed (if `T`=`rm`) or added (if `T`=`add`) from the real model to find the hypothetical one |

**Output predicates:**

| Name           | Description       |
| :------------- | :----------------- |
| `node(A)`    | Atom `A` is a node in the contrastive graph |
| `edge(A,B)`    | There is an edge in the contrastive graph from `A` to `B` |
| [`attr(T,X,A,V)`](#attrtxav) | The node/edge `X` has attribute `A` set to `V` |


<!-- **Reference predicates:**

| Name        | Description       |
| :---------- | :----------------- |
| `_model(real,A)` | `A` is obtained by solving the program as it was given. What is in input, is assumed to be naturally true. What is not in input, is assumed to be naturally false. |
| `_model(hypothetical,A)` | `A` is true in the hypothetical world we are reasoning about. The certainty/falsity of the atom may come from what is natural or from the assumptions we may make in the hypothetical world. | -->


### `abduction.lp`


??? quote "Source code"

    ```prolog
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Finds the hypothetical model using abduction

    #defined _abduced/2.

    :- _query(exclude,Atom), _model(hypothetical,Atom).
    :- _query(include,Atom), not _model(hypothetical,Atom).

    world(real;hypothetical).

    {_abduced(X,Atom)} :- _abducible(X,Atom).

    %=== Constraints

    % (C1) No sense to remove something that is not in input
    :- not _model(real,Atom), _abduced(rm,Atom).
    % (C2) + (C4) No sense to both remove and add something
    :- _abduced(add,Atom), _abduced(rm,Atom).
    % (C3) No sense to add something that is already in input
    :- _model(real,Atom), _abduced(add,Atom).

    _model(hypothetical,Atom) :- _abduced(add, Atom).

    %=== Distance

    :~ _distance(N,D,L). [D@L,N]

    % Default distance
    % _distance((Atom,h), 1, 0) :- _model(hypothetical, Atom), not _model(real, Atom).
    % _distance((Atom,r), 1, 0) :- _model(real, Atom), not _model(hypothetical, Atom).

    ```

!!! asp-doc "ASP Doc"

    Finds the hypothetical model using abduction

    ``` prolog
    #defined _abduced/2.

    :- _query(exclude,Atom), _model(hypothetical,Atom).
    :- _query(include,Atom), not _model(hypothetical,Atom).

    world(real;hypothetical).

    {_abduced(X,Atom)} :- _abducible(X,Atom).
    ```

    === "Constraints"

        ``` prolog
        :- not _model(real,Atom), _abduced(rm,Atom). %(1)!
        :- _abduced(add,Atom), _abduced(rm,Atom). %(2)!
        :- _model(real,Atom), _abduced(add,Atom). %(3)!
        _model(hypothetical,Atom) :- _abduced(add, Atom).
        ```

        1.  :speech_balloon: (C1) No sense to remove something that is not in input
        2.  :speech_balloon: (C2) + (C4) No sense to both remove and add something
        3.  :speech_balloon: (C3) No sense to add something that is already in input

    === "Distance"

        ``` prolog
        :~ _distance(N,D,L). [D@L,N]
        ```

### `contrastive.lp`


??? quote "Source code"

    ```prolog
    % Marks relevant atoms of the program, with respect of the atoms that must be explained.
    % TODO: for now this is marking all atoms as relevant.
    _relevant(W, Atom) :- _model(W, Atom).

    %=== Firable

    % fireable if abduced
    _fbody(_abduced, hypothetical, Atom, ()) :- _abduced(add, Atom).
    % fireable if fact
    _fbody(R, W, Atom, Vars) :- _relevant(W, Atom), _sup(R, W, Atom, Vars), not _depends(_sup(R, W, _, _), _).
    % firable if supported body.
    _fbody(R, W, Atom, Vars) :-
        _sup(R, W, Atom, Vars),
        _f_atom(W, Cause) : _depends(_sup(R, W, Atom, Vars), Cause).

    % Decides which rule fire each relevant atom in the graph (must be one and only one).
    {_f(R, W, Atom, Vars) : _fbody(R, W, Atom, Vars)} :- _relevant(W, Atom).

    :- _f(ID1, W, Atom, _), _f(ID2, W, Atom, _), ID1!=ID2.
    :- _relevant(W, Atom), not _f_atom(W,Atom).

    _f_atom(W, Atom) :- _f(_, W, Atom, _).

    %=== Causes and inhibitors

    % Captures positive body for this graph
    _direct_cause(R, W, Effect, Cause) :-
        _f(R, W, Effect, Vars),
        _depends(_sup(R, W, Effect, Vars), Cause).

    % Captures negative body for this graph
    _direct_inhibitor(R, W, Effect, Inhibitor) :-
        _f(R, W, Effect, Vars),
        _prevents(_sup(R, W, Effect, Vars), Inhibitor).

    ```


!!! asp-doc "ASP Doc"

    ```prolog
    _relevant(W, Atom) :- _model(W, Atom). %(1)!
    ```

    1.  :speech_balloon: Marks relevant atoms of the program, with respect of the  atoms that must be explained.

        !!! question

            TODO: for now this is marking all atoms as relevant.



    === "Fireable"

        ```prolog

        _fbody(_abduced, hypothetical, Atom, ()) :- _abduced(add, Atom). %(1)!
        _fbody(R, W, Atom, Vars) :- _relevant(W, Atom), _sup(R, W, Atom, Vars), not _depends(_sup(R, W, _, _), _). %(2)!
        _fbody(R, W, Atom, Vars) :-
            _sup(R, W, Atom, Vars),
            _f_atom(W, Cause) : _depends(_sup(R, W, Atom, Vars), Cause). %(3)!


        {_f(R, W, Atom, Vars) : _fbody(R, W, Atom, Vars)} :- _relevant(W, Atom). %(4)!

        :- _f(ID1, W, Atom, _), _f(ID2, W, Atom, _), ID1!=ID2.
        :- _relevant(W, Atom), not _f_atom(W,Atom).

        _f_atom(W, Atom) :- _f(_, W, Atom, _).
        ```

        1.  :speech_balloon: fireable if abduced
        2.  :speech_balloon: fireable if fact
        3.  :speech_balloon: fireable if supported body
        4.  :speech_balloon: Decides which rule fire each relevant atom in the graph (must be one and only one).


    === "Causes and inhibitors"

        ```prolog

        _direct_cause(R, W, Effect, Cause) :-
            _f(R, W, Effect, Vars),
            _depends(_sup(R, W, Effect, Vars), Cause). %(1)!

        _direct_inhibitor(R, W, Effect, Inhibitor) :-
            _f(R, W, Effect, Vars),
            _prevents(_sup(R, W, Effect, Vars), Inhibitor).%(2)!
        ```


        1.  :speech_balloon: Captures positive body for this graph
        2.  :speech_balloon: Captures negative body for this graph


### `graphs.lp`


??? quote "Source code"

    ```prolog
    % Creates the graph based on the causes and inhibitors

    %=== Nodes
    node(Atom):-_f_atom(W, Atom).
    attr(node,Atom,origin,W):- _f_atom(W, Atom).
    attr(node,Atom,abduced,X):- node(Atom), _abduced(X,Atom).
    attr(node,Atom,query,X):- node(Atom), _query(X,Atom).

    %=== Edges
    edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
    attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).

    edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
    attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
    attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).

    ```


!!! asp-doc "ASP Doc"


    === "Nodes"

        ```prolog

        node(Atom):-_f_atom(W, Atom).
        attr(node,Atom,origin,W):- _f_atom(W, Atom).
        attr(node,Atom,abduced,X):- node(Atom), _abduced(X,Atom).
        attr(node,Atom,query,X):- node(Atom), _query(X,Atom).
        ```

    === "Edges"

        ```prolog

        edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
        attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).

        edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).
        ```

### Glossary

<!-- Could come from something like clorm or be typed in the code -->
#### `attr(T,X,A,V)`

Attributes for the graph elements.

=== "T=`node`"

    - `origin`: either `real` or `hypothetical`
    - `abduced`: either `rm` or `add`
    - `query`: either `include` or `exclude`

=== "T=`edge`"

    - `origin`: either `real` or `hypothetical`
    - `type`: either `inhibitor` or `cause`
