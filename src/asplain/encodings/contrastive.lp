%*
Computes the contrastive graph based on the found hypothetical model

!!! question "TODO"
    Do we want to mark atoms that are relevant or just provide the full graph?


# _xclingo_f_atom(World, Atom)
    Means that `Atom` is a node in the `World` explanation graph.
    -Atom: a node in the graph.
    -World: can be `real` or `hypothetical`.

# _xclingo_direct_cause(RuleID, World, Effect, Cause)
    Models the directed edge `Cause -> Effect` that belongs to the graph `World`.
    -RuleID: the identifier of the rule after which the edge was modeled.
    -World: can be `real` or `hypothetical`.
    -Effect: the destination node of the directed edge.
    -Cause: the source node of the directed edge.

# _xclingo_direct_inhibitor(RuleID, World, Effect, Inhibitor)
    Captures the Inhibitor-Effect relation between a negative literal in the body of a rule and an atom in the head. This is used for linking the Reference and the Contrastive explanation as the inhibitors of an atom that is in one graph will appear in the other graph.
    -RuleID: the identifier of the rule after which the edge was modeled.
    -World: can be `real` or `hypothetical`.
    -Effect: the destination node of the directed edge.
    -Inhibitor: the source node of the directed edge.
*%

% At the moment we are not marking the atoms that are relevant, we are just providing the full graph.
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

_model_negators(C, Vars,  A1, A2) :-
    _constraints((C, Vars), A1), _constraints((C, Vars), A2), A1!=A2.
