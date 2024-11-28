# LLMs

- LLMs can be used to make natural language from explanation graphs

## Interactive integration

- If they LLMS are integrated into something like clinguin, they can have information about the interactive process
- Also the LLMs could respond the atoms that were used in the expiation provided, this way the UI can add highlights and hints about the explanation to complement the natural language response with visual input.

## Short and long answers

- A short answer might skip steps
- Only when asked the long answer could be provided

## How to prompt the LLM?

- We need a fixed input format
- We need at least 5-10 examples with expected short and long explanations
- We need examples that cover all cases
- We need to find out what other information the LLM will need
    - What was the query
    - What was in all the models
    - What was abduced
    - What is the original program
    - Meaning of predicates

## Prompt idea


Hey! I am creating a system to generate explanation graphs of why an atom is or isn't part of an ASP program. This is how it works:

Input:
    - program: An ASP logic program that solves your problem
    - model: A stable model (which is a set of true atoms)
    - query: The query states what the user wanted on the model. It can be atoms that the should be part of the model or atoms that should not be part of the model.
    - explanation prefernce: Decides which atoms from the input could potentially be removed or added.

Output:
    - A contrastive explanation graph, this graph will have nodes and edges with different attributes. It represents the contrast between the explanation graph for the given model `real` and the explanation graph for the found model `hypothetical` that makes the query true. Therefor the nodes of the contrasted contrastive graph all the union of the nodes of the two other graphs. The attribute `origin` tells from which graph they come, which could be both.
    This graph has two type of edges (X,Y):
      - normal ones for which the attribute `type` is `cause`, this means that the atom X  is a cause for atom Y.
      - inhibitor ones for which the attribute `type` is `inhibitor` Means that X prevented Y to be true.
    Additionally, the graph indicates which atoms had to be added or removed to get the hypothetical graph. This is defined with attribute `abduced` whose value can be `rm` for removed and `add` for added. This are the things that had to be changed. If nothing had to be changed it means that there was another model filling the needs stated in the query.

    The the definition of  `attr(T,X,A,V)` is the following:

        Attributes for the graph elements.

        === "T=`node`" then `X` is a node

            - `A=origin`: `V` is either `real` or `hypothetical`
            - `A=abduced`: `V` is either `rm` or `add`
            - `A=query`: `V` is either `include` or `exclude`

        === "T=`edge`" then `X` is an edge

            - `A=origin`: `V` is either `real` or `hypothetical`
            - `A=type`: `V` is either `inhibitor` or `cause`

    If the hypothetical and real graphs are the same, then the query was already part of the first graph and the explanation is the things that implied the query.


What I want you to do is the following:

I will give you:
- the contrastive graph using predicates `node`, `edge` and `attr`
- the original program
- the meaning of the atoms

I want you to give me an explanation in natural language for my query using the given graph.

Notice that from the graph you can infer the query using attr. As well as the original model using the nodes that have origin `real`.

Here are some examples, for all examples I will be using the same program and meaning

Program:

        p :- d, not a.
        a :- not h.
        d.
        h.

Meaning:

    p: James is poisoned
    d: A drug is given to James
    a: James is administered antidote a
    h: James is on holidays

Example 1:

    Graph:

        node(d).
        node(h).
        node(p).
        attr(edge,(d,p),type,cause).
        attr(edge,(d,p),origin,real).
        attr(node,p,query,exclude).
        attr(node,d,abduced,rm).
        attr(node,h,origin,hypothetical).
        attr(node,d,origin,real).
        attr(node,h,origin,real).
        attr(node,p,origin,real).
        edge(d,p).

    Expected response:

        For James to not be poisoned he would have to not been drudged.

Example 2:

    Graph:

        node(h).
        node(p).
        node(a).
        attr(edge,(d,p),type,cause).
        attr(edge,(a,p),type,inhibitor).
        attr(edge,(h,a),type,inhibitor).
        attr(edge,(d,p),origin,real).
        attr(node,p,query,exclude).
        attr(node,h,abduced,rm).
        attr(node,d,origin,hypothetical).
        attr(node,a,origin,hypothetical).
        attr(node,d,origin,real).
        attr(node,h,origin,real).
        attr(node,p,origin,real).
        edge(a,p).
        edge(h,a).
        edge(d,p).

    Expected response:


        For James to not be poisoned he would have to not have been in holidays.


    Alternative detailed  response:


        For James to not be poisoned he would have to not have been in holidays.
        If we hadn't been in holidays he would have been given the antidote which would have prevented him from being poisoned.

Example 3: (Both graphs are the same)

    Graph:



        node(d).
        node(h).
        node(p).
        attr(edge,(d,p),type,cause).
        attr(edge,(d,p),origin,real).
        attr(edge,(d,p),origin,hypothetical).
        attr(node,p,query,include).
        attr(node,d,origin,hypothetical).
        attr(node,h,origin,hypothetical).
        attr(node,p,origin,hypothetical).
        attr(node,d,origin,real).
        attr(node,h,origin,real).
        attr(node,p,origin,real).
        edge(d,p).

    Expected response:


        James was poisoned because he was drudged


Do you need any more information or can you work with this?


### First task



Program:

    person(gabriel;clare).

    drive(gabriel).
    resist(gabriel).

    drive(clare).

    punish(P) :- drive(P), alcohol(P),  person(P).
    punish(P) :- resist(P), person(P).

    sentence(P, prison) :- punish(P).
    sentence(P, innocent) :- person(P), not punish(P).

Meaning:

    person(X): X is a person
    drive(X): X drove
    resist(X): X resisted the authority
    alcohol(X): X had alcohol
    punish(X): X was punished
    sentence(X, prison): X was sentence to prison
    sentence(X, innocent): X was innocent

Graph:

    node(alcohol(gabriel)).
node(person(gabriel)).
node(person(clare)).
node(drive(gabriel)).
node(drive(clare)).
node(punish(gabriel)).
node(sentence(gabriel,prison)).
node(sentence(gabriel,innocent)).
node(sentence(clare,innocent)).
attr(edge,(person(clare),sentence(clare,innocent)),type,cause).
attr(edge,(person(gabriel),sentence(gabriel,innocent)),type,cause).
attr(edge,(punish(gabriel),sentence(gabriel,prison)),type,cause).
attr(edge,(person(gabriel),punish(gabriel)),type,cause).
attr(edge,(drive(gabriel),punish(gabriel)),type,cause).
attr(edge,(alcohol(gabriel),punish(gabriel)),type,cause).
attr(edge,(punish(gabriel),sentence(gabriel,innocent)),type,inhibitor).
attr(edge,(person(clare),sentence(clare,innocent)),origin,hypothetical).
attr(edge,(person(gabriel),sentence(gabriel,innocent)),origin,hypothetical).
attr(edge,(drive(gabriel),punish(gabriel)),origin,real).
attr(edge,(alcohol(gabriel),punish(gabriel)),origin,real).
attr(edge,(person(gabriel),punish(gabriel)),origin,real).
attr(edge,(person(clare),sentence(clare,innocent)),origin,real).
attr(edge,(punish(gabriel),sentence(gabriel,prison)),origin,real).
attr(node,sentence(gabriel,innocent),query,include).
attr(node,alcohol(gabriel),abduced,rm).
attr(node,person(gabriel),origin,real).
attr(node,person(gabriel),origin,hypothetical).
attr(node,person(clare),origin,real).
attr(node,person(clare),origin,hypothetical).
attr(node,drive(gabriel),origin,real).
attr(node,drive(gabriel),origin,hypothetical).
attr(node,alcohol(gabriel),origin,real).
attr(node,drive(clare),origin,real).
attr(node,drive(clare),origin,hypothetical).
attr(node,sentence(gabriel,innocent),origin,hypothetical).
attr(node,sentence(clare,innocent),origin,hypothetical).
attr(node,sentence(clare,innocent),origin,real).
attr(node,punish(gabriel),origin,real).
attr(node,sentence(gabriel,prison),origin,real).
edge(punish(gabriel),sentence(gabriel,innocent)).
edge(person(clare),sentence(clare,innocent)).
edge(person(gabriel),sentence(gabriel,innocent)).
edge(punish(gabriel),sentence(gabriel,prison)).
edge(person(gabriel),punish(gabriel)).
edge(drive(gabriel),punish(gabriel)).
edge(alcohol(gabriel),punish(gabriel)).

### Second task

Graph:

    node(resist(gabriel)).
    node(person(gabriel)).
    node(person(clare)).
    node(drive(gabriel)).
    node(drive(clare)).
    node(punish(gabriel)).
    node(sentence(gabriel,prison)).
    node(sentence(gabriel,innocent)).
    node(sentence(clare,innocent)).
    attr(edge,(person(clare),sentence(clare,innocent)),type,cause).
    attr(edge,(person(gabriel),sentence(gabriel,innocent)),type,cause).
    attr(edge,(punish(gabriel),sentence(gabriel,prison)),type,cause).
    attr(edge,(resist(gabriel),punish(gabriel)),type,cause).
    attr(edge,(person(gabriel),punish(gabriel)),type,cause).
    attr(edge,(punish(gabriel),sentence(gabriel,innocent)),type,inhibitor).
    attr(edge,(person(clare),sentence(clare,innocent)),origin,hypothetical).
    attr(edge,(person(gabriel),sentence(gabriel,innocent)),origin,hypothetical).
    attr(edge,(resist(gabriel),punish(gabriel)),origin,real).
    attr(edge,(person(gabriel),punish(gabriel)),origin,real).
    attr(edge,(person(clare),sentence(clare,innocent)),origin,real).
    attr(edge,(punish(gabriel),sentence(gabriel,prison)),origin,real).
    attr(node,sentence(gabriel,innocent),query,include).
    attr(node,resist(gabriel),abduced,rm).
    attr(node,person(gabriel),origin,real).
    attr(node,person(gabriel),origin,hypothetical).
    attr(node,person(clare),origin,real).
    attr(node,person(clare),origin,hypothetical).
    attr(node,drive(gabriel),origin,real).
    attr(node,drive(gabriel),origin,hypothetical).
    attr(node,resist(gabriel),origin,real).
    attr(node,drive(clare),origin,real).
    attr(node,drive(clare),origin,hypothetical).
    attr(node,sentence(gabriel,innocent),origin,hypothetical).
    attr(node,sentence(clare,innocent),origin,hypothetical).
    attr(node,sentence(clare,innocent),origin,real).
    attr(node,punish(gabriel),origin,real).
    attr(node,sentence(gabriel,prison),origin,real).
    edge(punish(gabriel),sentence(gabriel,innocent)).
    edge(person(clare),sentence(clare,innocent)).
    edge(person(gabriel),sentence(gabriel,innocent)).
    edge(punish(gabriel),sentence(gabriel,prison)).
    edge(resist(gabriel),punish(gabriel)).
    edge(person(gabriel),punish(gabriel)).
