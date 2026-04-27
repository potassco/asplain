% @label("The solution has value {} in position ({},{})",(N,X,Y,)) :: sudoku(X,Y,N)
% @label("The problem has the initial value {} at position ({},{})",(N,X,Y,)) :: initial(X,Y,N)
% @label("The cell ({},{}) is part of subgrid {}",(X1,Y1,S)) :: subgrid(X1,Y1,S)
% @label("{} is a number",(N,)) :: number(N)

dim(dim).
number(1..dim*dim).

% @label("Initals assign cell ({},{}) the value {}",(X,Y,N,))
sudoku(X,Y,N) :- initial(X,Y,N).
% @label("Choose a value for cell ({},{})",(X,Y,))
{sudoku(X,Y,N): number(N)} :- number(X), number(Y).
% Cardinality
% @label("Cell ({},{}) cannot have two different values",(X,Y,))
% @hide
:- number(X), number(Y), sudoku(X,Y,N), sudoku(X,Y,N2), N>N2.
% @label("Cell ({},{}) has value {} so it's defined",(X,Y,V,))
% @hide
defined(X,Y):- sudoku(X,Y,V).
% @label("Cell ({},{}) has to be defined",(X,Y,))
% @hide
:- number(X), number(Y), not defined(X,Y).

%## Sudoku Rules

% @label("Number {} cannot be multiple times in the row {}, but appears in columns {} and {}",(N,Y,X1,X2,))
:- sudoku(X1,Y,N), sudoku(X2,Y,N), X1>X2.
% @label("Number {} cannot be multiple times in the column {}, but appears in rows {} and {}",(N,X,Y1,Y2,))
:- sudoku(X,Y1,N), sudoku(X,Y2,N), Y1>Y2.

% @label("Cell ({},{}) is in subgrid {}",(X,Y,S,))
subgrid(X,Y,S) :- number(X), number(Y), S=(((X-1)/dim)*dim+((Y-1)/dim)).
% @label("Subgrid {} cannot have value {} in both cell ({},{}) and ({},{})",(S,V,X,Y,X2,Y2,))
:- sudoku(X,Y,V), sudoku(X2,Y2,V), subgrid(X,Y,S), subgrid(X2,Y2,S), (X,Y)<(X2,Y2).

#show sudoku/3.
#show initial/3.
