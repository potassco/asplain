# Contrastive explanation

A contrastive explanation compares a reference model to a contrasted model.


## Interpret the graphical visualization

- The graph for the reference model is found in blue.
- The graph for the contrasted model is found in green.
- The contrastive graph shows the color of the node depending which graph it originally belonged to. Additionally, nodes that were part of the reference graph but not of the contrasted model have a lower opacity.
- Normal edges aro those present in the reference graph.
- Dotted edges correspond to inhibitor edges.
- The query is shown with a thicker border
- Abduced atoms are shown crossed out if they where removed and underlined if they were added

!!! example

    See the full [James Bond](../examples/james-bond) example for details on the problem input.

    ![James Bond](../../../assets/images/james-bond-1.png){width="500"}

    In the example above, the query is : *I want a model without p*. So the hypothetical model fulfils this query by not having the node `p` in the graph. In the contrastive model the nodes `h` and `p` are with a lower opacity because they are not in the hypothetical one. `h` appears crossed out since it had to be removed from he input
