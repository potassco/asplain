
_distance(Atom, 1, 1) :-
    _abduced(_, Atom).

% --- Only initial positions can be removed.
_abducible(rm, h(on(Block),Position,0)):- _model(real, h(on(Block), Position, 0)), Block!=Position.

_abducible(add, h(on(Block),Position,0)) :-
    _model(real,n(N)),  % issue with constants
    Block=1..N,
    Position=1..N,
    Block!=Position.
_abducible(add, h(on(Block),table,0)) :-
    _model(real,n(N)),  % issue with constants
    Block=1..N.

% Forces to add an initial position for any block we have removed its initial position
:- _abduced(rm, h(on(Block), _, 0)), not _abduced(add, h(on(Block), _, 0)).

% If query asks about new step limits then you can abduce new step limits
_abducible((rm;add), last(Last)) :-
    Last=1..30.

%%%%%%%%%%%%%%% SITUATION
%
% This is the initial position
%                     h(on(4),1,0).
%                     h(on(1),3,0).
% h(on(2),table,0).   h(on(3),table,0).
%
% And this is the final positon that is eventually reached in 3 steps.
%                     g(on(2),1).
%                     g(on(1),4).
% g(on(3),table).     g(on(4),table).
%
% The user asks why there is no way to solve it 2 steps
%
% Query: h(on(2),1,2) h(on(1),4,2) h(on(3),table,2) h(on(4),table,2).
%
