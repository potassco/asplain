---
icon: material/tag
---

In *asplain* logic programs need to be annotated for explanations to be configured accordingly.
These annotations are done via tags.
These tags are comments that start with `% @`.

## Annotating rules vs atoms

### Rules

A rule is annotated by placing the tag in the line above the rule.

!!! example "Rule annotation example"

    The rule `head :- body.` is annotated as follows:

    ```clingo
    % @addable
    head :- body.
    ```

### Atoms
An atom is annotated by placing the tag in the same line as the atom, separated by `::`.

!!! example "Atom annotation example"

    The atom `atom.` is annotated as follows:
    ```clingo
    % @label("My atom") :: atom
    ```

!!! example "Atom with variables"

    The atoms matching `atom(X)` are as follows:
    ```clingo
    % @label("My atom with variable {}",(X,)) :: atom(X)
    ```

    This will annotate all atoms matching `atom(X)` with a label that includes the value of the variable `X` in the rule where the atom appears.

!!! warning "Note"

    Notice no dot '.' is added in the end of the comment.

## Built-in tags

Asplain comes with a range of predefined tags that can be used for annotating your program.:

### `@label(L)`

- Adds a label `L`
- Variables from the rule can be used in the label by providing them as a tuple in the second argument of the tag, e.g., `(X,Y,)` for variables `X` and `Y`.

!!! example "Label example"

    ```clingo
    % @label("{} is innocent since they were not punished",(P,))
    sentence(P, prison) :- punish(P).
    ```


!!! example "Label atom"

    ```clingo
    % @label("Person {} likes the pet {}",(P,A,)) :: person(P,A)
    ```

### `@addable`

- Makes a rule a candidate to be added as a change to the program
- In the [foil finding process](../foils.md) the rule might be added to the program to find a foil satisfying the query

!!! example

```clingo
% @addable
head :- body.
```

!!! warning "Note"

    Only rules are considered for the `@addable` and `@removable` tags, not atoms.
    If you want to make a fact of an atom removable you can either tag the fact itself or use [Dynamic Tags](#dynamic-tags) to Add rules.


### `@removable`

- Makes a rule a candidate to be removed as a change to the program
- In the [foil finding process](../foils.md) the rule might be removed from the program to find a foil satisfying the query

!!! example

```clingo
% @removable
head :- body.
```


!!! warning "Note"

    Only rules are considered for the `@addable` and `@removable` tags, not atoms.
    If you want to make a fact of an atom removable you can either tag the fact itself or use [Dynamic Tags](#dynamic-tags) to Add rules.

### `@hide`

- Hides the rule below in the contrastive explanation

!!! example

```clingo
% @hide
head :- body.
```

## Custom tags

You can use anything as a tag and then give it a meaning in an [explanation preference](../preferences/) or have different
dynamic annotations based on the tags, see the [Dynamic Annotations](#dynamic-annotations) section for more details.

!!! example "Custom tag example"


    ```clingo
    % @my_custom_tag
    :- a, b.
    ```

    ```clingo
    tag(label,removable):-tag(N,my_custom_tag).
    ```

## Dynamic Annotations

Annotations can also be added dynamically in an ASP encoding.
This encoding is then provided under the `--dynamic-tags` option in the CLI.

To do so, the rules can generate atoms of the form `tag(N, <TAG>)` where `N` is a unique identifier for the rule and `<TAG>` is the tag to be added to that rule.
You can use other tags or any information that is part og the program graph.


!!! Example "Removable assumptions"

    For example, if you want to make assumptions removable you can add the following rules in a separate encoding provided under the `--dynamic-tags` option:

    ```clingo
    tag(label,"Assumed"):-tag(N,assume(_)).
    tag(N,removable):-tag(N,assume(_)).
    ```

    First we label all assumptions with the label "Assumed" and then we make them removable by adding the `removable` tag to all rules that have an `assume` tag.



!!! Example "Removable atoms"

    You can use dynamic tags to make atoms removable by adding rules that add the `removable` tag to all rules that have that atom in the head and are facts, for example:

    This is part of the [Sudoku Example](../../examples/sudoku)

    ```clingo
    tag(R, removable):-
        A = initial(X,Y,V),
        node(A, atom),
        tag(R, fact),
        edge((R,A),1).
    ```

    Making all rules `R` removable if they are facts that have an atom `A` in the head that matches `initial(X,Y,V)`.
