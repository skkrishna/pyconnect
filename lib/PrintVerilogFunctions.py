def mkCase(inpVariable, events, spaceStr=None):
    strCase = ''
    strCase = strCase + "case(" + inpVariable + ")\n"
    if (spaceStr):
        strCase = spaceStr + strCase
        evntSpaceStr = spaceStr + "\t"
    else:
        evntSpaceStr = "\t"
    for (state, evnts) in events:
        eventStr =  state + ": begin\n" + evntSpaceStr + evnts + ";\n" + evntSpaceStr + "end\n"
        eventStr = evntSpaceStr + eventStr
        strCase = strCase + eventStr
    
    if (spaceStr):
        strCase = strCase + spaceStr + "endcase\n"
    else:
        strCase = strCase + "endcase\n"
    return strCase

def mkCondStmnt(cond, spaceStr=None):
    if (spaceStr):
        cussSpcStr = spaceStr
    else:
        cussSpcStr = ''
        
        
def mkAlwaysComb(events, addStr, spaceStr=None, typeFF=False):
    print("spaceStr = ", spaceStr,"|")
    strComb = ''
    strComb = strComb + "always_comb begin\n"
    print("strComb ", strComb)
    if (spaceStr):
        strComb = spaceStr + strComb
        evntSpaceStr = spaceStr + "\t"
    else:
        evntSpaceStr = "\t"
    if (typeFF):
        assgnType = " <= "
    else:
        assgnType = " = "
    for (var, evnts) in events:
        eventStr =  vat + assgnType + evnts + ";\n"
        eventStr = evntSpaceStr + eventStr
        strComb = strComb + eventStr
    strComb = strComb + addStr
    if (spaceStr):
        strComb = strComb + spaceStr + "end\n"
    else:
        strComb = strComb + "end\n"        
    return strComb

def mkAlwaysff(inpVars, events, clock, resetn, addStr, spaceStr=None):
    strFF = ''
    strFF = strFF + "always_ff @(posedge " + clock + "negedge " + resetn + ")  begin\n"
    if (spaceStr):
        strFF = spaceStr + strFF
        evntSpaceStr = spaceStr + "\t"
    else:
        evntSpaceStr = "\t"
    strFF = strFF + evntSpaceStr + "if !(" + resetn + ") begin\n"
    evntSpaceStr = evntSpaceStr + "\t"
    for var in (inpVars):
        eventStr =  var + " <= " + "'0;\n"
        eventStr = evntSpaceStr + eventStr
    if (spaceStr):
        strFF = strFF + spaceStr + "\t" + "end\n"
        strFF = strFF + spaceStr + "\t" + "else begin\n"
    else:
        strFF = strFF + "\t" + "end\n"
        strFF = strFF + "\t" + "else begin\n"
    for (var, evnts) in events:
        eventStr =  var + " <= " + evnts + ";\n"
        eventStr = evntSpaceStr + eventStr
        strFF = strFF + eventStr
    if (spaceStr):
        strFF = strFF + spaceStr + "\t" + "end\n"
    else:
        strFF = strFF + "\t" + "end\n"
    strFF = strFF + addStr
    if (spaceStr):
        strFF = spaceStr + strFF + "end\n"
    else:
        strFF = strFF + "end\n"        
    return strFF

def mkAssign(events, clock, resent, spaceStr=None):
    strAss = ''
    if (spaceStr):
        assSpace = spaceStr
    else:
        assSpace = ''
    for (var, evnts) in events:
        eventStr =  "assign " + var + " = " + evnts + ";\n"
        eventStr = assSpacer + eventStr
        strAss = strAss + eventStr
    return strAss

