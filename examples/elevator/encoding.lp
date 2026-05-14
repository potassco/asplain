% Elevator Temporal Example
%
% fluents : holds(F,T)    (F=fluent, T=timestep)
% actions : occur(A,T)    (A=action, T=timestep)
%         : action(A)
% time    : time(T)       (T=timestep)
%         : horizon(T)

% DEFINITIONS

time(0..horizon).

% Define actions
action(wait).
action(up).
action(down).
action(serve).
% Define fulents
% QUESTION : Does it make sense to include variables or arity in fluent definitions?
fluent(at).
fluent(serve).
fluent(served).
fluent(called).
fluent(ready).

% ACTION GENERATION

% Generate actions for each time step
{occur(A,T): action(A)} :- time(T),time(T+1).
% Cardinality constraints
% @label("At time {} there cannot be two actions {} and {} at the same time.",(T,A1,A2,))
:- time(T), time(T+1), occur(A1,T), occur(A2,T), A1!=A2.
has_action(T) :- occur(A,T).
% @label("At time {} there cannot be no action.",(T,))
:- time(T), time(T+1), not has_action(T).

% Eliminate invalid move actions
% TODO : Replace these with pre-conditions
% @label("The elevator cannot move up at time {} since it is already at the top floor {}",(T,X,))
:- occur(up,T),   holds(at(X),T), not floor(X+1).
% @label("The elevator cannot down up at time {} since it is already at the bottom floor {}",(T,X,))
:- occur(down,T), holds(at(X),T), not floor(X-1).

% CAUSAL RULES
% TODO : Specifically encode intertia

% Compute at positions from move actions
% @label("The elevator moves from floor {} up at time {} since action up is chosen",(X,T,))
holds(at(X+1),T+1) :- occur(up,T),   holds(at(X),T).
% @label("The elevator moves from floor {} down at time {} since action down is chosen",(X,T,))
holds(at(X-1),T+1) :- occur(down,T), holds(at(X),T).
% Compute at positions from wait and serve actions
% TODO : Overwork with inertia
% @label("The elevator doesn't change its floor at time {} since action wait is chosen",(T,))
holds(at(X),T+1) :- holds(at(X),T), occur(wait,T), time(T).
% @label("The elevator serves floor {} and doesn't change its positon at time {} since action serve is chosen",(X,T,))
holds(at(X),T+1) :- holds(at(X),T), occur(serve,T), time(T).

% Compute served
% QUESTION : Does it make sense / is it good pratice to define causal rules only using fluents and no actions?
holds(served(X),T) :- holds(at(X),T), occur(serve,T).
% Compute called
holds(called(X),T+1) :- holds(called(X),T), not holds(served(X),T), time(T).
% Compute ready
holds(ready,T) :- holds(called(X),T), holds(at(X),T).

% Only allow calling the elevator inside horizon
:- holds(called(X),T), not time(T).
