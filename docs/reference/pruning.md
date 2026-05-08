---
icon: material/scissors-cutting
---

Pruning can be used as a post-processing feature to reduce the size of the contrastive explanation graph.
For complex problems the size of the explanation graph can grow to a level where interpretation can be difficult.
For cases like this pruning can be useful to remove parts of the explanation that are unrelated or not necessary.
The applicability and usfulness of the different pruning approaches vary for different programs.

## Pruning Methods

### Orphans

This pruning method removes all orphan subgraphs that are not connected to the main subgraph which contains the __query__ and __changed__ nodes.
It is useful for removing parts of the contrastive graph that are not directly connected to main explanation.

```bash
asplain [...] --prune ORPHANS
```

::: src/asplain/encodings/pruning/orphans.lp
    handler: asp
    options:
        encodings:
            git_link: true
            include_title: false
        start_level: 4


### Paths

This pruning method finds paths over the contrastive graph edges connecting the __query__ and __changed__ nodes.
Only the nodes forming these paths are included after the pruning, since these are the nodes directly connecting the main elements of the explanation.

```bash
asplain [...] --prune PATHS
```

::: src/asplain/encodings/pruning/paths.lp
    handler: asp
    options:
        encodings:
            git_link: true
            include_title: false
        start_level: 4


### Changes

This pruning method only keeps the nodes that changed between the reference program and the found foil.
This method is especially useful for really large graphs where only focusing on the changed nodes can provide a clearer explanation.

!!! warning

    When the query is already satisfied in the reference model, this pruning method will not keep any nodes since there are no changes between the reference and the foil.

```bash
asplain [...] --prune CHANGES
```

::: src/asplain/encodings/pruning/changes.lp
    handler: asp
    options:
        encodings:
            git_link: true
            include_title: false
        start_level: 4
