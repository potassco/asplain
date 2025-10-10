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
{occur(A,T): action(A)}=1 :- time(T),time(T+1).

% Eliminate invalid move actions
% TODO : Replace these with pre-conditions
:- occur(up,T),   holds(at(X),T), not floor(X+1).
:- occur(down,T), holds(at(X),T), not floor(X-1).

% CAUSAL RULES
% TODO : Specifically encode intertia

% Compute at positions from move actions
holds(at(X+1),T+1) :- occur(up,T),   holds(at(X),T).
holds(at(X-1),T+1) :- occur(down,T), holds(at(X),T).
% Compute at positions from wait actions
% TODO : Overwork with inertia
holds(at(X),T+1) :- holds(at(X),T), not occur(up,T), not occur(down,T), time(T).
% Compute served
% QUESTION : Does it make sense / is it good pratice to define causal rules only using fluents and no actions?
holds(served(X),T) :- holds(at(X),T), holds(serve,T).
% Compute called
holds(called(X),T+1) :- holds(called(X),T), not holds(served(X),T).
% Compute ready
holds(ready,T) :- holds(called(X),T), holds(at(X),T).

% Only allow calling the elevator inside horizon
:- holds(called(X),T), not time(T).

