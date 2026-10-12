graph(elevator).

attr(node,N,fontname,"JetBrainsMono"):- node(N,_).


node(floor(F),elevator):- floor(F).
attr(node,floor(F),shape,square):- floor(F).
attr(node,floor(F),label,""):- floor(F).
attr(node,floor(F),width,"1"):- floor(F).
attr(node,floor(F),pos,@pos(0,F)):- floor(F).
attr(node,floor(F),penwidth,3):- floor(F).
attr(node,floor(F),color,"#455A64"):- floor(F).

node(floor_label(F),elevator):- floor(F).
attr(node,floor_label(F),label,@concat("<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0' CELLPADDING='0'><TR><TD HEIGHT='3'></TD></TR><TR><TD>",F,"</TD></TR></TABLE>>")):- floor(F), not called(F).
attr(node,floor_label(F),width,"0.5"):- floor(F).
attr(node,floor_label(F),height,"0.5"):- floor(F).
attr(node,floor_label(F),fixedsize,true):- floor(F).
attr(node,floor_label(F),pos,@pos(-1,F)):- floor(F).
attr(node,floor_label(F),penwidth,0):- floor(F).
attr(node,floor_label(F),style,filled):- floor(F).
attr(node,floor_label(F),fillcolor,"#B0BEC5"):- floor(F), not called(F).
attr(node,floor_label(F),fontcolor,"#607D8B"):- floor(F), not called(F).
attr(node,floor_label(F),fillcolor,"#E53935"):- floor(F), called(F).
attr(node,floor_label(F),fontcolor,"#FFEBEE"):- floor(F), called(F).
attr(node,floor_label(F),label,@concat("<<TABLE BORDER='0' CELLBORDER='0' CELLSPACING='0' CELLPADDING='0'><TR><TD HEIGHT='4'></TD></TR><TR><TD><B>",F,"</B></TD></TR></TABLE>>")):- floor(F), called(F).

node(elevator,elevator):- at(F).
attr(node,elevator,label,""):- at(F).
attr(node,elevator,shape,rectangle):- at(F).
attr(node,elevator,width,"0.7"):- at(F).
attr(node,elevator,height,"0.8"):- at(F).
attr(node,elevator,pos,@pos(0,F)):- at(F).
attr(node,elevator,penwidth,0):- at(F).
attr(node,elevator,style,filled):- at(F).
attr(node,elevator,fillcolor,"#78909C"):- at(F), not serve.
attr(node,elevator,fillcolor,"#66BB6A"):- at(F), serve.
