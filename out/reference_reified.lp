symbol_literal(d,3).
symbol_literal(a,10).
symbol_literal(h,6).
symbol_literal(w,7).
symbol_literal(p,17).
tag(rule(disjunction(0),normal(0)),program(base)).
tag(rule(disjunction(0),normal(0)),rule_fo("d.")).
tag(rule(choice(1),normal(1)),label("Bond might be holiday or working")).
tag(rule(choice(1),normal(1)),program(base)).
tag(rule(choice(1),normal(1)),rule_fo("{ h; w }.")).
tag(rule(disjunction(2),normal(2)),label("Bond receives the antidote if he is working")).
tag(rule(disjunction(2),normal(2)),program(base)).
tag(rule(disjunction(2),normal(2)),rule_fo("a :- w.")).
tag(rule(disjunction(3),normal(3)),label("Bond has to be either on holiday or working")).
tag(rule(disjunction(3),normal(3)),program(base)).
tag(rule(disjunction(3),normal(3)),rule_fo("#false :- not h; not w.")).
tag(rule(disjunction(3),normal(4)),label("Bond cannot be both on holiday and working")).
tag(rule(disjunction(3),normal(4)),program(base)).
tag(rule(disjunction(3),normal(4)),rule_fo("#false :- h; w.")).
tag(rule(disjunction(4),normal(5)),label("Bond is poisoned if he drinks the drug and does not receive the antidote")).
tag(rule(disjunction(4),normal(5)),program(base)).
tag(rule(disjunction(4),normal(5)),rule_fo("p :- d; not a.")).
tag(atom(3),label("Bond has drunk the drug")).
tag(atom(10),label("Bond has received the antidote")).
tag(atom(6),label("Bond is on holiday")).
tag(atom(7),label("Bond is working")).
rule(disjunction(0),normal(0)).
rule(choice(1),normal(1)).
rule(disjunction(2),normal(2)).
rule(disjunction(3),normal(3)).
rule(disjunction(3),normal(4)).
rule(disjunction(4),normal(5)).
literal_tuple(2,7).
literal_tuple(4,7).
literal_tuple(4,6).
literal_tuple(5,3).
literal_tuple(10,3).
literal_tuple(11,10).
literal_tuple(12,6).
literal_tuple(13,7).
literal_tuple(14,17).
literal_tuple(3,-7).
literal_tuple(3,-6).
literal_tuple(5,-10).
literal_tuple(0).
literal_tuple(1).
literal_tuple(2).
literal_tuple(3).
literal_tuple(4).
literal_tuple(5).
literal_tuple(10).
literal_tuple(11).
literal_tuple(12).
literal_tuple(13).
literal_tuple(14).
atom_tuple(0,3).
atom_tuple(1,6).
atom_tuple(1,7).
atom_tuple(2,10).
atom_tuple(4,17).
atom_tuple(0).
atom_tuple(1).
atom_tuple(2).
atom_tuple(3).
atom_tuple(4).
