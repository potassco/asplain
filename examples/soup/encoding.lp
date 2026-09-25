% Soup Temporal Example

% @time(T) :: occur(A,T)
% @time(T) :: holds(F,T)
% @time(T) :: time(T)


time(0..horizon).

% Define actions
action(ll).
action(lr).
% Define fulents
fluent(full).
fluent(empty).

% ACTION GENERATION

% @label("At time {} action {} occurs",(T,A,))
% @time(T)
{occur(A,T): action(A)} :- time(T),time(T+1).

% @label("Action {} was prohibited in {}, so it cannot occur",(A,T,))
% @time(T)
:- prohibit(A,T), occur(A,T).

% CAUSAL RULES

% @label("The soup bowl was full and lifted only on the left in {}, so it spilled and became empty.",(T,))
% @time(T)
holds(empty,T+1) :- occur(ll,T), not occur(lr,T), holds(full,T), time(T+1).
% @label("The soup bowl was full and lifted only on the right in {}, so it spilled and became empty.",(T,))
% @time(T)
holds(empty,T+1) :- occur(lr,T), not occur(ll,T), holds(full,T), time(T+1).
% @label("The soup bowl was full and lifted on both sides in {}, so it stayed full.",(T,))
% @time(T)
holds(full,T+1) :- occur(lr,T), occur(ll,T), holds(full,T), time(T+1).

% INERTIA RULES

% @label("The soup bowl remains full in {} if no action occurs",(T,))
% @time(T)
% @inertia
holds(full,T+1) :- holds(full,T), not occur(_,T), time(T+1).
% @label("Once the soup bowl was empty in {}, it remains empty in {}",(T,T+1,))
% @time(T)
% @inertia
holds(empty,T+1) :- holds(empty,T), time(T+1).

% CONSTRAINTS

% @label("At time {} the soup bowl cannot both be both full and empty",(T,))
% @time(T)
:- holds(full,T), holds(empty,T).
