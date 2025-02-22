house(1..3).
color(red;green).

neighbours(A,B) :- house(A), house(B), A!=B, (A-B)**2=1.

% COLOR CHOICE
{assign(H, wall_color, C): color(C)} :- house(H).
{assign(H, roof_color, C): color(C)} :- house(H).

% CHOICE RULE CARDINALITIES
:- house(H), assign(H, wall_color, C1), assign(H, wall_color, C2), C1!=C2.
:- house(H), not assign(H, wall_color, red), not assign(H, wall_color, green).
:- house(H), assign(H, roof_color, C1), assign(H, roof_color, C2), C1!=C2.
:- house(H), not assign(H, roof_color, red), not assign(H, roof_color, green).

% NO NEIGHBOURING HOUSES WITH SAME WALL COLOR
:- assign(A, wall_color, C), assign(B, wall_color, C), neighbours(A,B), A<B.
% NO HOUSE WITH DIFFERING WALL AND ROOF COLORS
:- assign(A, wall_color, C1), assign(A, roof_color, C2), C1!=C2.


%assign(1,roof_color,red).
%assign(3,wall_color,red).