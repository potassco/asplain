variable("frontWheel","Wheel").
variable("rearWheel","Wheel").
domain("Wheel", ("W14";"W16";"W18";"W20")).

constraint("frontWheel=rearWheel").
binary("frontWheel=rearWheel","frontWheel","=","rearWheel").

% ---- Model
value("frontWheel","W18").
% value("rearWheel","W18").
