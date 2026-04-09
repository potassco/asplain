% # Count number of nodes and edges in a graph represented as ASP facts.
% > python -m clingo src/asplain/utils/node-count.lp out/reference_pg.lp

number(atom,S):- #sum {1,N: node(N,atom)} = S.
number(rule,S):- #sum {1,N: node(N,rule(_))} = S.

number(edge,S):- #sum {1,E: edge(E,_)} = S.

#show number/2.
