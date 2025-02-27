variable("frontWheel","Wheel").
variable("rearWheel","Wheel").
variable("color","Color").

domain("Wheel", (14;16;18;20)).
domain("Color", ("Red";"Blue";"Green";"Yellow")).

constraint("frontWheel=rearWheel").
binary("frontWheel=rearWheel","frontWheel","=","rearWheel").

% constraint("!color=Red||frontWheel>16").
binary("!color=Red||frontWheel>16","!color=Red","||","frontWheel>16").
unary("!color=Red","!","color=Red").
binary("color=Red","color","=","Red").
binary("frontWheel>16","frontWheel",">","16").
% Why is it only sat with this commented out?

value("Red","Red").
value("Green","Green").
value("Yellow","Yellow").
value("Blue","Blue").
value("16",16).
value("14",14).
value("18",18).
value("20",20).
