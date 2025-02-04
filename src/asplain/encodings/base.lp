%*
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
        _distance(Atom, 1, 1) :- _abduced(_, Atom).
        ```

    === "Query"

        The hypothetical model must include a

        ```
        _query(include,a),
        ```

    === "Abduction program"

        The input program reified to talk about worlds. This is done automatically by the system.

        ```
        _model(hypothetical,a) :- not _abduced(rm,a); not _model(hypothetical,b).
        _model(hypothetical,b) :- not _abduced(rm,b).
        ```

    === "Support program"

        The input program reified to talk support. This is done automatically by the system.

        ```
        _sup(1,World,a,()) :- world(World); not _model(World,b).
        _prevents(_sup(1,World,a,()),b) :- _sup(1,World,a,()).
        _sup(2,World,b,()) :- world(World).

*%

#include "abduction.lp".
#include "contrastive.lp".
#include "graphs.lp".
#include "reachable.lp".

% #show node/1.
% #show edge/3.
% #show attr/4.
#show .
#show node(N):node(N), reachable(node,N).
#show edge(N,N',ID):edge(N,N',ID), reachable(edge,ID).
#show attr(T,ID,A,N):attr(T,ID,A,N), reachable(T,ID).
