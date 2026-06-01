% Robots Temporal Example

% @time(T) :: occur(A,R,T)
% @time(T) :: holds(F,T)
% @time(T) :: time(T)
% @time(T) :: has_action(R,T)

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
% @label("At time {} there cannot be two actions {} and {} at the same time for the same robot {}.",(T,A1,A2,R,))
% @time(T)
:- time(T), time(T+1), occur(A1,R,T), occur(A2,R,T), A1!=A2.
% @hide
has_action(R,T) :- occur(A,R,T).
% @label("At time {} there cannot be no action for robot {}.",(T,R,))
% @time(T)
:- time(T), robot(R), time(T+1), not has_action(R,T).

% Eliminate invalid actions

% @label("Robot {} cannot move up from node ({},{}) at time {} since there is no node above",(R,X,Y,T,))
% @time(T)
:- occur(up,R,T), holds(at(R,(X,Y)),T), not node(X,Y-1).
% @label("Robot {} cannot move down from node ({},{}) at time {} since there is no node below",(R,X,Y,T,))
% @time(T)
:- occur(down,R,T), holds(at(R,(X,Y)),T), not node(X,Y+1).
% @label("Robot {} cannot move left from node ({},{}) at time {} since there is no node to the left",(R,X,Y,T,))
% @time(T)
:- occur(left,R,T), holds(at(R,(X,Y)),T), not node(X-1,Y).
% @label("Robot {} cannot move right from node ({},{}) at time {} since there is no node to the right",(R,X,Y,T,))
% @time(T)
:- occur(right,R,T), holds(at(R,(X,Y)),T), not node(X+1,Y).

% Initial positions

% @label("Robot {} starts at node ({},{})",(R,X,Y,))
% @time(0)
holds(at(R,(X,Y)),0) :- start(R,(X,Y)).

% Compute at positions
% @label("Robot {} moves up from ({},{}) to ({},{}) at time {}",(R,X,Y,X,Y-1,T,))
% @time(T)
holds(at(R,(X,Y-1)),T+1) :- occur(up,R,T),  holds(at(R,(X,Y)),T).
% @label("Robot {} moves down from ({},{}) to ({},{}) at time {}",(R,X,Y,X,Y+1,T,))
% @time(T)
holds(at(R,(X,Y+1)),T+1) :- occur(down,R,T),  holds(at(R,(X,Y)),T).
% @label("Robot {} moves left from ({},{}) to ({},{}) at time {}",(R,X,Y,X-1,Y,T,))
% @time(T)
holds(at(R,(X-1,Y)),T+1) :- occur(left,R,T),  holds(at(R,(X,Y)),T).
% @label("Robot {} moves right from ({},{}) to ({},{}) at time {}",(R,X,Y,X+1,Y,T,))
% @time(T)
holds(at(R,(X+1,Y)),T+1) :- occur(right,R,T),  holds(at(R,(X,Y)),T).
% @label("Robot {} waits at ({},{}) at time {}",(R,X,Y,T,))
% @time(T)
holds(at(R,(X,Y)),T+1) :- occur(wait,R,T),  holds(at(R,(X,Y)),T).

% @label("Robot {} reached its goal node ({},{}) at time {}",(R,X,Y,T,))
% @time(T)
holds(reached_goal(R),T) :- holds(at(R,(X,Y)),T), goal(R,(X,Y)).

% @label("Inertia for fluent reached_goal at time {}",(T,))
% @time(T)
holds(reached_goal(R),T+1) :- holds(reached_goal(R),T), time(T+1).

% CONSTRAINTS

% @label("Robot {} has to have reached its goal node at the time horizon {}",(R,horizon,))
% @time(horizon)
:- robot(R), not holds(reached_goal(R),horizon).

% @label("Robot {} and {} cannot be both at node {} at time {} (Vertex Conflict)",(R1,R2,POS,T,))
% @time(T)
:- holds(at(R1,POS),T), holds(at(R2,POS),T), R1>R2.

% @label("Robot {} and {} cannot switch positions ({} <-> {}) between timesteps {} and {} (Edge Conflict)",(R1,R2,POS1,POS2,T,T+1,))
% @time(T)
:- holds(at(R1,POS1),T), holds(at(R1,POS2),T+1), holds(at(R2,POS2),T), holds(at(R2,POS1),T+1), R1>R2.
