# Contrastive Explanation

??? info "clindoc"

    How the documentation for this page could be automatically generated

    ```
    ::: encodings/base.lp
        :root-file: false
        :source: true
        :predicate-table: true
        :dependency-graph: true
        :glosary: true
        :subfiles: true
        :glossary-references: true

    ```

    - **root-file:** If the root file name is included, in this case it is not

    - **source:** Shows the content of the source file (like mkdocstring)
        - The example of the source I only left in the first file, the rest don't have it, in favor of the github link

    - **predicate-table:** Adds a table with the summary of all preicates
        - The summary table could be generated with chatgpt
    - **dependency-graph:** Adds a dependency graph using mermaid. Dependency graph can be automatically computed perhaps with more detailed arrows
    - **glossary:** Adds a section with the glossary of all predicates used
        - Perhaps the definition of atoms could be taken from clorm instead (if there is one)
    - **glossary-references:** Adds a reference sections in each predicate of the glossary
        - Perhaps we also want to include references from instances as examples...
    - **subfiles:** Includes all of the included files



Computes the contrastive graphs using abduction. A contrastive graph will compare a reference model with a hypothetical which fulfils a query.

??? example "Example Input"

    === "Model"
        The reference model containing only `b`
        ```
        _model(real, b).
        ```

    === "Abducibles"
        `b` can be removed from the reference model
        ```
        _abducible(rm,b).
        ```

    === "Distance"
        Each atom abduced will be penalized
        ```
        distance(Atom, 1, 1) :- abduced(_, Atom).
        ```

    === "Query"
        The hypothetical model must include a
        ```
        _query(include,a),
        ```

    === "Abduction program"
        The input program reified to talk about worlds. This is done automatically by the system.
        ```
        _model(hypothetical,a) :- not abduced(rm,a); not _model(hypothetical,b).
        _model(hypothetical,b) :- not abduced(rm,b).
        ```

    === "Support program"
        The input program reified to talk support. This is done automatically by the system.
        ```
        _sup(1,World,a,()) :- world(World); not _model(World,b).
        _prevents(_sup(1,World,a,()),b) :- _sup(1,World,a,()).
        _sup(2,World,b,()) :- world(World).
        ```



??? quote "Source"

    ```prolog
    #include "abduction.lp".
    #include "contrastive.lp".
    #include "graphs.lp".

    #show node/1.
    #show edge/2.
    #show attr/4.
    ```

??? asp-doc "Encoding"

    ```prolog
    #include "abduction.lp".
    #include "contrastive.lp".
    #include "graphs.lp".

    #show node/1.
    #show edge/2.
    #show attr/4.
    ```


| Predicate | Description | Type |
| :-------- | :---------- | :--- |
| [`_abducible(T,A)`](#_abducibleta) | Abducible atoms | <span style="color:#9178C6"> :material-arrow-right-bold:</span> |
| [`distance(N,D,L)`](#_distancendl) | Distance between the real and hypothetical model | <span style="color:#9178C6"> :material-arrow-right-bold:</span> |
| [`_query(T,A)`](#_queryta) | Query that should hold in the hypothetical model | <span style="color:#9178C6"> :material-arrow-right-bold:</span> |
| [`_model(T,A)`](#_modelta) | Atoms that are part of the model | <span style="color:#9178C6"> :material-arrow-right-bold:</span> |
| [`abduced(T,A)`](#abducedta) | Uses the concept of abduction to find the hypothetical model | :material-eye-closed: |
| [`_f_atom(W, A)`](#_f_atomwa) | Means that `A` is a node in the `W` explanation graph | :material-eye-closed: |
| [`_direct_cause(R, W, E, C)`](#_direct_causerwec) | Models the directed edge `C -> E` that belongs to the graph `W` | :material-eye-closed: |
| [`_direct_inhibitor(R, W, E, I)`](#_direct_inhibitorrwei) | Captures the Inhibitor-E relation between a negative literal in the body of a rule and an atom in the head | :material-eye-closed: |
| [`node(A)`](#nodea) | Defines a node in the graph | <span style="color:#52BF54">:material-eye:</span> |
| [`edge(N,N')`](#edgenn) | Defines an edge in the graph | <span style="color:#52BF54">:material-eye:</span> |
| [`attr(T,N,A,V)`](#attrtnav) | Defines an attribute for a node or edge | <span style="color:#52BF54">:material-eye:</span> |


``` mermaid
flowchart LR
    ab(["_abducible/2"])
    di(["distance/3"])
    q(["_query/2"])
    m(["_model/2"])
    f(["_f_atom/2"])
    abduced(["abduced/2"])
    d(["_direct_cause/4"])
    i(["_direct_inhibitor/4"])
    n(["node/1"])
    e(["edge/2"])
    a(["attr/4"])
    m --> m
    m --> f
    di --> m
    q --> m
    ab --> abduced
    m --> abduced
    abduced --> m
    m --> i
    m --> d
    f --> n
    d --> e
    i --> e
    abduced --> a
    m --> a
    classDef all fill:#00000000
    class ab,di,q,m,f,abduced,d,i,n,e,a, all;
    classDef in stroke:#9178C6,stroke-width:3px;
    class ab,di,q,m in;
    classDef out stroke:#52BF54,stroke-width:3px;
    class n,e,a out;
    classDef aux stroke:#848484,stroke-width:0.2px;
    class f,abduced,d,i, aux;
```

<br/>


### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-encoding"></code> [:material-github:](https://github.com/potassco/asplain/blob/master/src/asplain/encodings/abduction.lp) `abduction.lp`


Finds the hypothetical model using abduction and the distance defined by the user


??? asp-doc "Encoding"

    ``` prolog
    #defined abduced/2.

    :- _query(exclude,Atom), _model(hypothetical,Atom).
    :- _query(include,Atom), not _model(hypothetical,Atom).

    world(real;hypothetical).

    {abduced(X,Atom)} :- _abducible(X,Atom).
    ```

    === "Constraints"

        ``` prolog
        :- not _model(real,Atom), abduced(rm,Atom). %(1)!
        :- abduced(add,Atom), abduced(rm,Atom). %(2)!
        :- _model(real,Atom), abduced(add,Atom). %(3)!
        _model(hypothetical,Atom) :- abduced(add, Atom).
        ```

        1.  :speech_balloon: (C1) No sense to remove something that is not in input
        2.  :speech_balloon: (C2) + (C4) No sense to both remove and add something
        3.  :speech_balloon: (C3) No sense to add something that is already in input

    === "Distance"

        ``` prolog
        :~ distance(N,D,L). [D@L,N]
        ```
<br/>

### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-encoding"></code> [:material-github:](https://github.com/potassco/asplain/blob/master/src/asplain/encodings/contrastive.lp) `contrastive.lp`


Computes the contrastive graph based on the found hypothetical model

!!! question "TODO"
    Do we want to mark atoms that are relevant or just provide the full graph?


??? asp-doc "Encoding"

    ```prolog
    _relevant(W, Atom) :- _model(W, Atom). %(1)!
    ```

    1.  :speech_balloon: Marks relevant atoms of the program, with respect of the  atoms that must be explained.

        !!! question

            TODO: for now this is marking all atoms as relevant.



    === "Fireable"

        ```prolog

        _fbody(abduced, hypothetical, Atom, ()) :- abduced(add, Atom). %(1)!
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

<br/>

### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-encoding"></code> [:material-github:](https://github.com/potassco/asplain/blob/master/src/asplain/encodings/graphs.lp) `graphs.lp`

Creates the graph based on the causes and inhibitors


??? asp-doc "Encoding"

    === "Nodes"

        ```prolog

        node(Atom):-_f_atom(W, Atom).
        attr(node,Atom,origin,W):- _f_atom(W, Atom).
        attr(node,Atom,abduced,X):- node(Atom), abduced(X,Atom).
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

<br/>

---------

## :material-format-list-bulleted-square: Glossary



#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_abducible(T,A)`
Abducible atoms

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `T`       | Type of abduction `add` or `rm`    |
| `A`       | Atom that can be abduced           |

??? asp-doc-ref "References"

    === "`abduction.lp`"

        ```prolog hl_lines="1"
        {abduced(X,Atom)} :- _abducible(X,Atom).
        ```
<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `distance(N,D,L)`
Distance between the real and hypothetical model.

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `N`       | Identifier for the distance        |
| `D`       | Penalization value                 |
| `L`       | Level of the distance              |

??? asp-doc-ref "References"

    === "`abduction.lp`"

        ```prolog
        :~ distance(N,D,L). [D@L,N]
        ```
<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_query(T,A)`
Query that should hold in the hypothetical model

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `T`       | Type of query `include` or `exclude` |
| `A`       | Atom that the user wants to include or exclude |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog
        :- _query(exclude,Atom), _model(hypothetical,Atom).
        :- _query(include,Atom), not _model(hypothetical,Atom).
        ```

    === "`abduction.lp`"

        ```prolog
        attr(node,A,query,X):- node(A), _query(X,A).
        ```


<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_model(T,A)`
Atoms that are part of the model

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `T`       | Type of model `real` or `hypothetical` |
| `A`       | Atom that is part of the model     |

??? asp-doc-ref "References"

    === "`abduction.lp`"

        ```prolog hl_lines="4"
        :- _query(exclude,Atom), _model(hypothetical,Atom).
        :- _query(include,Atom), not _model(hypothetical,Atom).
        :- not _model(real,Atom), abduced(rm,Atom).
        _model(hypothetical,Atom) :- abduced(add, Atom).
        ```

    === "`graph.lp`"

        ```prolog
        :- _query(exclude,Atom), _model(hypothetical,Atom).
        :- _query(include,Atom), not _model(hypothetical,Atom).
        ```

    === "`contrastive.lp`"

        ```prolog
        attr(node,A,query,X):- node(A), _query(X,A).
        ```


<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `abduced(T,A)`
Uses the concept of abduction to find the hypothetical model

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `T`       | Type of abduction `add` or `rm`    |
| `A`       | Atom that has been abduced         |

??? asp-doc-ref "References"

    === "`abduction.lp`"

        ```prolog hl_lines="1"
        {abduced(X,Atom)} :- _abducible(X,Atom).
        :- not _model(real,Atom), abduced(rm,Atom).
        :- abduced(add,Atom), abduced(rm,Atom).
        :- _model(real,Atom), abduced(add,Atom).
        ```

    === "`graph.lp`"

        ```prolog
        attr(node,A,abduced,X):- node(A), abduced(X,A).
        ```

    === "`contrastive.lp`"

        ```prolog
        _fbody(abduced, hypothetical, Atom, ()) :- abduced(add, Atom).
        ```


<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_f_atom(W, A)`
Means that `A` is a node in the `W` explanation graph.

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `W`       | Can be `real` or `hypothetical`    |
| `A`       | A node in the graph                |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog
        node(A):-_f_atom(W, A).
        attr(node,A,origin,W):- _f_atom(W, A).
        ```

    === "`contrastive.lp`"

        ```prolog hl_lines="5"
        _fbody(R, W, Atom, Vars) :-
            _sup(R, W, Atom, Vars),
            _f_atom(W, Cause) : _depends(_sup(R, W, Atom, Vars), Cause).
        :- _relevant(W, Atom), not _f_atom(W,Atom).
        _f_atom(W, Atom) :- _f(_, W, Atom, _).

        ```


<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_direct_cause(R, W, E, C)`
Models the directed edge `C -> E` that belongs to the graph `W`.

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `R`       | Identifier of the rule             |
| `W`       | Can be `real` or `hypothetical`    |
| `E`       | Effect destination node            |
| `C`       | Cause source node                  |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog
        edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
        attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).
        attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).
        ```

    === "`contrastive.lp`"

        ```prolog hl_lines="1 2 3"
        _direct_cause(R, W, Effect, Cause) :-
            _f(R, W, Effect, Vars),
            _depends(_sup(R, W, Effect, Vars), Cause).
        ```

<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `_direct_inhibitor(R, W, E, I)`
Captures the Inhibitor-E relation between a negative literal in the body of a rule and an atom in the head.

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `R`       | Identifier of the rule             |
| `W`       | Can be `real` or `hypothetical`    |
| `E`       | Destination node                   |
| `I`       | Source node                        |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog
        edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        ```

    === "`contrastive.lp`"

        ```prolog hl_lines="1-3"
        _direct_inhibitor(R, W, Effect, Inhibitor) :-
            _f(R, W, Effect, Vars),
            _prevents(_sup(R, W, Effect, Vars), Inhibitor).
        ```

<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `node(A)`
Defines a node in the graph

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `A`       | Node identifier (atom)             |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog hl_lines="1"
        node(A):-_f_atom(W, A).
        attr(node,A,abduced,X):- node(A), abduced(X,A).
        attr(node,A,query,X):- node(A), _query(X,A).
        edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        ```

<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `edge(N,N')`
Defines an edge in the graph. They represent the causal relationships between nodes, as well as negative relationships (inhibitors).

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `N`       | Origin node                        |
| `N'`      | Destination node                   |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog hl_lines="1"
        edge(Cause,Effect):-_direct_cause(RuleID, W, Effect, Cause).
        edge(Cause,Effect):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).

        ```

<br/>

#### <code class="doc-symbol doc-symbol-heading doc-clingo-symbol-predicate"></code> `attr(T,N,A,V)`
Defines an attribute for a node or edge.

| Parameter | Description                        |
| :-------- | :--------------------------------- |
| `T`       | Type of the element (`node` or `edge`) |
| `N`       | Node or edge identifier            |
| `A`       | Attribute name                     |
| `V`       | Attribute value                    |

??? asp-doc-ref "References"

    === "`graph.lp`"

        ```prolog hl_lines="1-6"
        attr(node,A,origin,W):- _f_atom(W, A).
        attr(node,A,abduced,X):- node(A), abduced(X,A).
        attr(node,A,query,X):- node(A), _query(X,A).
        attr(edge,(Cause,Effect),origin,W):-_direct_cause(RuleID, W, Effect, Cause).
        attr(edge,(Cause,Effect),type,inhibitor):-_direct_inhibitor(RuleID, W, Effect, Cause), node(Effect), node(Cause).
        attr(edge,(Cause,Effect),type,cause):-_direct_cause(RuleID, W, Effect, Cause).
        ```
