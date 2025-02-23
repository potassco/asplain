time(1..3).
{tired(T)}:-time(T).
{rain(T)}:-time(T).
dirty(T+1):-rain(T),time(T+1).
do(clean,T):-dirty(T), not tired(T).
dirty(T+1):-dirty(T), not do(clean,T),time(T+1).
