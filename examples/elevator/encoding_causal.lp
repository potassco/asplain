#const horizon=15.
time(0..horizon).

% Generate causal actions for each time step
{wait(T); up(T) ; down(T); serve(T)}=1 :- time(T+1),time(T).
{wait(T)}  :- time(T+1),time(T).
% Up is possible if not on top
{up(T)}    :- time(T+1),time(T), at(X,T), floor(X2), X2>X.
% Down is possible if not on bottom
{down(T)}  :- time(T+1),time(T), at(X,T), floor(X2), X2<X.
% Serve is possible if called and at right floor
{serve(T)} :- time(T+1),time(T), called(X,T2), not served(X,T2), at(X,T), T>=T2.
% Allow only one action at a time
:- C=#count{wait(T),up(T),down(T),serve(T)}, time(T), C!=1.


% Eliminate invalid move actions
:- up(T),   at(X,T), not floor(X+1), time(T).
:- down(T), at(X,T), not floor(X-1), time(T).

% Compute at positions from move actions
at(X+1,T+1):- up(T),   at(X,T), time(T).
at(X-1,T+1):- down(T), at(X,T), time(T).
% Compute at positions from wait actions
at(X, T+1)  :- at(X,T), not up(T), not down(T), time(T).
% Compute served
served(X, T) :- at(X,T), serve(T).
% Compute called
called(X,T+1):- called(X,T), time(T), not served(X, T).
% Compute ready
ready(T) :- called(X,T), at(X,T).

% Only allow calling the elevator inside horizon
:- called(X,T), not time(T).