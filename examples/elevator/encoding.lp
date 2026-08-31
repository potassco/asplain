% Elevator Temporal Example

% @time(T) :: occur(A,T)
% @time(T) :: holds(F,T)
% @time(T) :: time(T)
% @time(T) :: has_action(T)


time(0..horizon).

% Define actions
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

% @label("At time {} action {} occurs",(T,A,))
% @time(T)
{occur(A,T): action(A)} :- time(T),time(T+1).
% @label("At time {} there cannot be two actions {} and {} at the same time.",(T,A1,A2,))
% @time(T)
:- time(T), time(T+1), occur(A1,T), occur(A2,T), A1!=A2.

% ACTION CONDITIONS

% @label("The elevator cannot move up at time {} since it is already at the top floor {}",(T,X,))
% @time(T)
:- occur(up,T),   holds(at(X),T), not floor(X+1).
% @label("The elevator cannot down up at time {} since it is already at the bottom floor {}",(T,X,))
% @time(T)
:- occur(down,T), holds(at(X),T), not floor(X-1).

% CAUSAL RULES

% Compute at positions from move actions
% @label("The elevator moves from floor {} up at time {} since action up is chosen",(X,T,))
% @time(T)
holds(at(X+1),T+1) :- occur(up,T),   holds(at(X),T).
% @label("The elevator moves from floor {} down at time {} since action down is chosen",(X,T,))
% @time(T)
holds(at(X-1),T+1) :- occur(down,T), holds(at(X),T).
% @label("The elevator serves floor {} and doesn't change its positon at time {} since action serve is chosen",(X,T,))
% @time(T)
holds(at(X),T+1) :- holds(at(X),T), occur(serve,T), time(T).
% @label("Serve floor {} at time {} when serve action occurs on floor {}",(X,T,X))
% @time(T)
holds(served(X),T) :- holds(at(X),T), occur(serve,T).
% Compute ready
% @label("The elevator is ready at time {} if at that time is was called to floor {} and also is at that floor",(T,X,))
% @time(T)
holds(ready,T) :- holds(called(X),T), holds(at(X),T).

% INERTIA RULES

% @label("The elevator doesn't change its floor at time {} since action wait is chosen",(T,))
% @time(T)
% @inertia
holds(at(X),T+1) :- holds(at(X),T), not occur(up,T), not occur(down,T), time(T).
% @label("Call elevator for floor {} at {} if elevator was called before and not served",(X,T+1,))
% @time(T)
% @inertia
holds(called(X),T+1) :- holds(called(X),T), not holds(served(X),T), time(T).


% Only allow calling the elevator inside horizon
% @label("The elevator cannot be called at time {}, because it is outside the allowed timesteps",(T,))
% @time(T)
:- holds(called(X),T), not time(T).
