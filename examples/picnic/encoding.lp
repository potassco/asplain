% @label("It is sunny") :: s
% @label("It is raining") :: r
% @label("Jane brought an umbrella") :: u
% @label("A picnic takes place") :: p

s.

% @label("It may start raining")
{r}.

% @label("A picnic takes place because it is sunny and not raining")
p :- s, not r.

% @label("A picnic takes place in the rain because Jane brought an umbrella")
p :- r, u.

#program asplain.
% @addable
u.
