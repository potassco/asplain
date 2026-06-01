% Robots Temporal Example

% @time(T) :: occur(A,T)
% @time(T) :: holds(F,T)
% @time(T) :: time(T)
% @time(T) :: has_action(T)

time(0..horizon).

% Actions
action(wait).
action(up).
action(down).
action(left).
action(right).

% Fulents
fluent(at).
fluent(reached_goal).

% ACTION GENERATION

% @time(T)
{occur(A,R,T): action(A)} :- robot(R), time(T), time(T+1).
% Cardinality constraints
% @time(T)
:- time(T), time(T+1), occur(A1,R,T), occur(A2,R,T), A1!=A2.
% @hide
has_action(R,T) :- occur(A,R,T).
% @time(T)
:- time(T), robot(R), time(T+1), not has_action(R,T).

% Eliminate invalid actions

% @time(T)
:- occur(up,R,T), holds(at(R,(X,Y)),T), not node(X,Y-1).
% @time(T)
:- occur(down,R,T), holds(at(R,(X,Y)),T), not node(X,Y+1).
% @time(T)
:- occur(left,R,T), holds(at(R,(X,Y)),T), not node(X-1,Y).
% @time(T)
:- occur(right,R,T), holds(at(R,(X,Y)),T), not node(X+1,Y).

% Initial positions

% @time(0)
holds(at(R,(X,Y)),0) :- start(R,(X,Y)).

% Compute at positions
% @time(T)
holds(at(R,(X,Y-1)),T+1) :- occur(up,R,T),  holds(at(R,(X,Y)),T).
% @time(T)
holds(at(R,(X,Y+1)),T+1) :- occur(down,R,T),  holds(at(R,(X,Y)),T).
% @time(T)
holds(at(R,(X-1,Y)),T+1) :- occur(left,R,T),  holds(at(R,(X,Y)),T).
% @time(T)
holds(at(R,(X+1,Y)),T+1) :- occur(right,R,T),  holds(at(R,(X,Y)),T).
% @time(T)
holds(at(R,(X,Y)),T+1) :- occur(wait,R,T),  holds(at(R,(X,Y)),T).

% Compute rached_goal
% @time(T)
holds(reached_goal(R),T) :- holds(at(R,(X,Y)),T), goal(R,(X,Y)).

% Inertia
% @time(T)
holds(reached_goal(R),T+1) :- holds(reached_goal(R),T), time(T+1).

% CONSTRAINTS

% All robots must reach goal their goal
% @time(horizon)
:- robot(R), not holds(reached_goal(R),horizon).

% Vertex Conflict
% @time(T)
:- holds(at(R1,POS),T), holds(at(R2,POS),T), R1>R2.

% Edge Conflict
% @time(T)
:- holds(at(R1,POS1),T), holds(at(R1,POS2),T+1), holds(at(R2,POS2),T), holds(at(R2,POS1),T+1), R1>R2.
