%%%%%%%%%%%%%% xclingo_fired_contrastive.lp %%%%%%%%%%%%%%%%%

%% xclingo implementation of
% https://www.cambridge.org/core/services/aop-cambridge-core/content/view/542C1AA568113B703F179D15E3CBB3EE/S1471068424000048a.pdf/model_explanation_via_support_graphs.pdf
% but it includes:
% - abduced atoms.
% - contrastive worlds real and hypothetical.
% - inhibitors (https://arxiv.org/abs/1602.06897).

% _xclingo_model(real,Atom) :- real(Atom).
% _xclingo_model(hypothetical,Atom) :- hypothetical(Atom).

% Marks relevant atoms of the program, with respect of the atoms that must be explained.
% TODO: for now this is marking all atoms as relevant. Should adapt the real xclingo implementation.
_xclingo_relevant(W, Atom) :- _xclingo_model(W, Atom).

%%%% fireable if abduced
_xclingo_fbody(_abduced, hypothetical, Atom, ()) :- _xclingo_abduced(add, Atom).
%%%% fireable if fact
_xclingo_fbody(RuleID, World, Atom, Vars) :- _xclingo_relevant(World, Atom), _xclingo_sup(RuleID, World, Atom, Vars), not _xclingo_depends(_xclingo_sup(RuleID, World, _, _), _).
%%%% firable if supported body.
_xclingo_fbody(R, W, Atom, Vars) :-
    _xclingo_sup(R, W, Atom, Vars),
    _xclingo_f_atom(W, Cause) : _xclingo_depends(_xclingo_sup(R, W, Atom, Vars), Cause).

% Decides which rule fire each relevant atom in the graph (must be one and only one).
{_xclingo_f(RuleID, World, Atom, Vars) : _xclingo_fbody(RuleID, World, Atom, Vars)} :- _xclingo_relevant(World, Atom).

:- _xclingo_f(ID1, W, Atom, _), _xclingo_f(ID2, W, Atom, _), ID1!=ID2.
:- _xclingo_relevant(W, Atom), not _xclingo_f_atom(W,Atom).

_xclingo_f_atom(World, Atom) :- _xclingo_f(_, World, Atom, _).

% Captures positive body for this graph
_xclingo_direct_cause(RuleID, World, Effect, Cause) :-
    _xclingo_f(RuleID, World, Effect, Vars),
    _xclingo_depends(_xclingo_sup(RuleID, World, Effect, Vars), Cause).

% Captures negative body for this graph
_xclingo_direct_inhibitor(RuleID, World, Effect, Inhibitor) :-
    _xclingo_f(RuleID, World, Effect, Vars),
    _xclingo_prevents(_xclingo_sup(RuleID, World, Effect, Vars), Inhibitor).
