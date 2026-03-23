%  Encoding for a 4x4 sudoku

% Input
% @label("The solution has value {} in position ({},{})",(N,X,Y,)) :: sudoku(X,Y,N)
% @label("The problem has the initial value {} at position ({},{})",(N,X,Y,)) :: initial(X,Y,N)
% @label("The cell ({},{}) is part of subgrid {}",(X1,Y1,S)) :: subgrid(X1,Y1,S)
% @label("{} is a number",(N,)) :: number(N)

#const dim=2.

number(1..2**2).
% @label("Each initial value has to be in the solution")
sudoku(X,Y,N) :- initial(X,Y,N).
% @label("Each cell is assigned a value")
{sudoku(X,Y,N): number(N)} :- number(X), number(Y).
% Cardinality
% @label("Each cell can only have one value")
:- number(X), number(Y), sudoku(X,Y,N), sudoku(X,Y,N2), N>N2.
% @label("Each filled cell is marked as defined")
defined(X,Y):- sudoku(X,Y,V).
% @label("Every cell has to be defined")
:- number(X), number(Y), not defined(X,Y).
% Sudoku Rules
% @label("Each number is only allowed once per row")
:- sudoku(X1,Y,N), sudoku(X2,Y,N), X1>X2.
% @label("Each number is only allowed once per column")
:- sudoku(X,Y1,N), sudoku(X,Y2,N), Y1>Y2.

% @label("Each cell is assigned to a subgrid")
subgrid(X,Y,(((X-1)/dim)*dim+((Y-1)/dim))) :- number(X), number(Y).
% @label("Each number is only allowed once per subgrid")
:- sudoku(X,Y,V), sudoku(X',Y',V), subgrid(X,Y,S), subgrid(X',Y',S), (X,Y)!=(X',Y').

#show sudoku/3.
#show initial/3.
