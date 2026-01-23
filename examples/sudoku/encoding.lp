%  Encoding for a 4x4 sudoku

% Input
% @label("The solution has value {} in position ({},{})",(N,X,Y,)) :: sudoku(X,Y,N)
% @label("The problem has the initial value {} at position ({},{})",(N,X,Y,)) :: initial(X,Y,N)
% @label("The cells ({},{}) and ({},{}) are in the same subgrid",(X1,Y1,X2,Y2,)) :: subgrid(X1,Y1,X2,Y2)
% @label("{} is a number",(N,)) :: number(N)

number(1..4).
sudoku(X,Y,N) :- initial(X,Y,N).
{sudoku(X,Y,N): number(N)} :- number(X), number(Y).
% Cardinality
:- number(X), number(Y), sudoku(X,Y,N), sudoku(X,Y,N2), N>N2.
defined_sudoku(X,Y):- sudoku(X,Y,V). %Bacause can't use _
:- number(X), number(Y), not defined_sudoku(X, Y).
% Sudoku Rules
:- sudoku(X1,Y,N), sudoku(X2,Y,N), X1>X2.
:- sudoku(X,Y1,N), sudoku(X,Y2,N), Y1>Y2.

subgrid(X,Y,(((X-1)/dim)*dim+((Y-1)/dim))) :- pos(X,Y).
:- sudoku(X,Y,V), sudoku(X',Y',V), subgrid(X,Y,S), subgrid(X',Y',S), (X,Y)!=(X',Y').

initial(1,1,1). initial(4,2,2). initial(2,3,1). initial(3,4,2).

#show sudoku/3.
#show initial/3.
