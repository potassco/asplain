---
icon: material/head-dots-horizontal
---

# Problem specification

We think of an explanation tool for ASP as something that is capable of explaining (given a stable model), why something is/isn't part of the model.

The computed information is in the form of an [explanation graph](#explanation-graph)

## :material-graph-outline: Explanation Graph

An explanation graph $G=(N,E)$ is composed of nodes $N$ and edges $E$.

Additionally it includes functions $f_N$ and $f_E$ to specify attributes to the nodes and edges. This attributes will depend on the type of explanation computed.

### ASP syntax

An explanation graph is defined in ASP via facts using predicates `node/1` `edge/2` and `attr/4`.

- `node(N)` Adds a node to the graph identified by `N`
- `edge(N1,N2)` Adds an edge to the graph from `N1` to `N2`
- `attr(node,N,ATTR,VALUE)` Adds attribute `ATTR` with value `VALUE` to node `N`
- `attr(edge,(N1,N2),ATTR,VALUE)` Adds attribute `ATTR` with value `VALUE` to edge `N1` to `N2`

!!! Example

    ``` prolog
    node(a).
    node(b).
    edge(a,b).
    attr(node,a,type,fact).
    attr(edge,(a,b),rule,1).
    ```


    ``` mermaid
    graph LR
    A((a)) --> B((b));
    ```

## :material-palette: Clingraph visualization

We provide a default [clingraph][clingraph] encoding to visualize such graphs.

This encoding can be overwritten by any custom explanation.

[clingraph]: https://clingraph.readthedocs.io/en/latest/
