location(O,D,T) :- occurs(E,T-1), instance(E,move), event_agent(E,O), event_destination(E,D).
