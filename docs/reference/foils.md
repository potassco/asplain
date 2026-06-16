---
icon: "material/head-question"
---

# Foil finding

Foil finding is the step where *asplain* builds an alternative version of the program that matches the user's expectation.
The original program is the **reference** program.
The alternative one is the **foil** program.

In simple terms, *asplain* answers a question such as _"Why not `p`?"_ by looking for a small, controlled change to the reference program that makes `p` true.
That changed program, together with one of its answer sets, is called a **foil**.

## What a foil is

A foil is made from:

- the reference program,
- a set of rules that may be **added**,
- a set of rules that may be **removed**,
- and a query describing what the user expected.

The result must satisfy two conditions:

- it only changes the program using the allowed additions and removals,
- it has an answer set in which the query holds.

If the reference program already has an answer set satisfying the query, then no change is needed: the reference program itself can serve as the foil.

If no allowed change can produce a program satisfying the query, then no foil exists and *asplain* cannot generate a contrastive explanation.

## Why optional rules matter

Foil finding is intentionally restricted.
*asplain* does not change arbitrary parts of the program.
It only works with the rules marked as optional:

- **addable rules** may be inserted into the foil,
- **removable rules** may be deleted from the reference program.

This keeps the explanation meaningful because the system only explores changes that the user or application considers relevant.

This is set via annotations in the logic program, which are described in the [Tagging Reference](../tagging/index.md).

## Simple intuition

Suppose the user expects atom `p` to be true, but no answer set of the reference program contains `p`.
Then *asplain* searches for a nearby version of the program where `p` does hold.

Typical outcomes are:

- removing a rule that blocks `p`,
- adding a rule that derives `p`,
- or combining both kinds of changes.

Different foils may satisfy the same query.
Each foil gives a different contrastive view of what would need to change for the expected outcome to appear.

## Unsatisfiable programs

Foil finding also works when the reference program has no answer set.
In that case, the goal may simply be to recover satisfiability.

If the query is empty, *asplain* looks for an allowed modification that makes the program satisfiable again.
Any answer set of that repaired program can then be used as the foil model.

## Choosing one foil

There can be many valid foils.
*asplain* therefore ranks them with a [**cost function**](../preferences) and selects the most suitable one.
Details on this pro

The exact cost function can vary, but the general idea is simple:
prefer foils that provide the most useful explanation of how the reference world differs from the expected one.

To compare both worlds, *asplain* records:

- which rules belong to the reference program, the foil program, or both,
- and which atoms hold in the reference model, the foil model, or both.

This information is later used to build the [contrastive explanation graph](./explanation-graph/index.md).
