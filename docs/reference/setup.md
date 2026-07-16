---
icon: "material/tools"
---

# Setup

The setup is constructed from the reification of a [tagged program](./tagging.md) and contains all the information needed to find the explanations (foils).

## Program graph

The basis of every explanation is the program graph, a directed graph that fully encodes a ground logic program.
It contains a node for every atom and every rule of the program:

- __Atom nodes__ represent the atoms of the program.
- __Rule nodes__ represent the rules and are typed as either `choice` or `disjunction` rules. Facts and integrity constraints are special cases of disjunctive rules.

The edges connect rules with the atoms they depend on and derive:

- An edge from an atom to a rule means the atom appears in the rule's body. The edge is __positive__ for positive body literals and __negative__ for negative ones (`not a`).
- An edge from a rule to an atom means the atom appears in the rule's head.

As a consequence, facts appear as rule nodes without incoming edges, while integrity constraints appear as rule nodes without outgoing edges.

### Reference program vs foil program

To use the same program graph for both the reference and foil program, the setup construction uses a single program graph that contains all rules and atoms of both programs.
The membership of each rule and atom in the reference and foil program is encoded via predicate `program(R, W)`, where `R` is a rule and `W` is either `ref` or `foil`.
For the setup we only use `ref` and `foil` is introduced later during foil finding.

## Removable and addable rules

The setup construction also identifies the rules that can be removed from the reference program and those that can be added to it.
This is indicated via predicate `optional(C, R)`, where `C` is either `add` or `remove` and `R` is a rule.
Those atoms are extracted from the tagged program and are used to generate the set of candidate foils during foil finding.

## Query

The query (set of literals) is represented as a set of atoms with their expected truth value, which is indicated via predicate `query(A, V)`, where `A` is an atom and `V` is either `1` (true) or `0` (false).


## Implementation

In the implementation the setup is generated using the reification of a [tagged program](./tagging.md).

::: src/asplain/encodings/reify-to-pg.lp
    handler: asp
    options:
        encodings:
            git_link: true
            source: false
        predicate_table: true
        start_level: 3
