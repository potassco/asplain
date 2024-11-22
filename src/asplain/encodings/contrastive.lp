%%%%%%%%%%%%%% xclingo_fired_contrastive.lp %%%%%%%%%%%%%%%%%

%% xclingo implementation of
% https://www.cambridge.org/core/services/aop-cambridge-core/content/view/542C1AA568113B703F179D15E3CBB3EE/S1471068424000048a.pdf/model_explanation_via_support_graphs.pdf
% but it includes:
% - abduced atoms.
% - contrastive worlds real and hypothetical.
% - inhibitors (https://arxiv.org/abs/1602.06897).

% _model(real,Atom) :- real(Atom).
% _model(hypothetical,Atom) :- hypothetical(Atom).

% Marks relevant atoms of the program, with respect of the atoms that must be explained.
% TODO: for now this is marking all atoms as relevant. Should adapt the real xclingo implementation.
_relevant(W, Atom) :- _model(W, Atom).

%%%% fireable if abduced
_fbody(_abduced, hypothetical, Atom, ()) :- _abduced(add, Atom).
%%%% fireable if fact
_fbody(R, W, Atom, Vars) :- _relevant(W, Atom), _sup(R, W, Atom, Vars), not _depends(_sup(R, W, _, _), _).
%%%% firable if supported body.
_fbody(R, W, Atom, Vars) :-
    _sup(R, W, Atom, Vars),
    _f_atom(W, Cause) : _depends(_sup(R, W, Atom, Vars), Cause).

% Decides which rule fire each relevant atom in the graph (must be one and only one).
{_f(R, W, Atom, Vars) : _fbody(R, W, Atom, Vars)} :- _relevant(W, Atom).

:- _f(ID1, W, Atom, _), _f(ID2, W, Atom, _), ID1!=ID2.
:- _relevant(W, Atom), not _f_atom(W,Atom).

_f_atom(W, Atom) :- _f(_, W, Atom, _).

% Captures positive body for this graph
_direct_cause(R, W, Effect, Cause) :-
    _f(R, W, Effect, Vars),
    _depends(_sup(R, W, Effect, Vars), Cause).

% Captures negative body for this graph
_direct_inhibitor(R, W, Effect, Inhibitor) :-
    _f(R, W, Effect, Vars),
    _prevents(_sup(R, W, Effect, Vars), Inhibitor).
