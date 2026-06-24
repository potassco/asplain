%*! cost(Name, Value, Level)

Represents a cost that will be optimized when finding foils.

Args:
    - Name: A unique identifier for a cost that will be penalized.
    For example, if you want to penalize each added rule, you would create one cost/3 instance for each rule with the name of the rule as Name.
    - Value: A numeric value representing the cost to be penalized. Can be negative for rewards.
    - Level: A numeric value representing the priority of this cost. Higher levels are optimized first
*%
