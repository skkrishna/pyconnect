import sys,imp
import re
import argparse
import importlib

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Generate Verilog file from embedded verilog file .pv and the generated python file .py"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('files', nargs='*')
    parser.add_argument("--python", help="Keep commented python code",
                    action="store_true")
    return parser

def printWireSigns(fpsv, designObj, spaceStr="\t"):
    wireKeys = designObj.wires.keys()
    ioStatement = "\n"
    for signls in (wireKeys):
        sigWidth = designObj.wires[signls]
        if (sigWidth):
            ioLine = spaceStr + 'wire ' +  "[" + sigWidth[1] + " : " + sigWidth[0] + "] " + signls + ";\n"
        else:
            ioLine = spaceStr + 'wire ' + signls + ";\n"
        ioStatement  = ioStatement + ioLine
    fpsv.write(ioStatement)


def printInOutSigns(fpsv, designObj, spaceSize=0):
    spaceStr = ''
    for ns in range(spaceSize):
        spaceStr = spaceStr + ' '

    inpList = {}
    outList = {}
    ioStatement = ''
    ioLine = spaceStr + 'input logic ' +  designObj.clock + ",\n"
    ioStatement  = ioStatement + ioLine
    ioLine = spaceStr + 'input logic ' +  designObj.reset + ",\n"
    ioStatement  = ioStatement + ioLine
    for sigName, sigTpe, sigIntf in (designObj.siglist):
        #print(sigName, sigTpe, sigIntf)
        if (sigTpe == 'int_input'):
            if (sigIntf):
                ioLine = spaceStr + 'input logic ' +  "[" + sigIntf[1] + " : " + sigIntf[0] + "] " + sigName + ",\n"
            else:
                ioLine = spaceStr + 'input logic ' + sigName + ",\n"
        elif (sigTpe == 'int_output'):
            if (sigIntf):
                ioLine = spaceStr + 'output logic ' +  "[" + sigIntf[1] + " : " + sigIntf[0] + "] " + sigName + ",\n"
            else:
                ioLine = spaceStr + 'output logic ' + sigName + ",\n"
        elif (sigIntf):
            print(sigName, sigTpe, sigIntf)
            if (sigTpe == 'int_input'):
                ioLine = spaceStr + 'input logic ' +  "[" + sigIntf[1] + " : " + sigIntf[0] + "] " + sigName + ",\n"
            elif (sigTpe == 'int_output'):
                ioLine = spaceStr + 'output logic ' +  "[" + sigIntf[1] + " : " + sigIntf[0] + "] " + sigName + ",\n"
            else:
                iolist = designObj.intf[sigIntf].getConnections()
                inpList = iolist['inputs']
                outList = iolist['outputs']
        if ((sigTpe == 'input') or (sigTpe == 'output') or (sigTpe == 'clock') or (sigTpe == 'reset')):
            if (sigTpe == 'input'):
                if (sigIntf):
                    sigStr = sigIntf + "_" + sigName
                if (inpList[sigName]):
                    sigWidth = inpList[sigName]
                    ioLine = spaceStr + 'input logic ' +  "[" + sigWidth[1] + " : " + sigWidth[0] + "] " + sigStr + ",\n"
                else:
                    ioLine = spaceStr + 'input logic ' + sigStr + ",\n"
            elif (sigTpe == 'output'):
                if (sigIntf):
                    sigStr = sigIntf + "_" + sigName
                if (outList[sigName]):
                    sigWidth = outList[sigName]
                    ioLine = spaceStr + 'output logic ' +  "[" + sigWidth[1] + " : " + sigWidth[0] + "] " + sigStr + ",\n"
                else:
                    ioLine = spaceStr + 'output logic ' + sigStr + ",\n"
            else:
                ioLine = spaceStr + 'input logic ' + sigName + ",\n"
        ioStatement  = ioStatement + ioLine
    ioStatement = ioStatement[0:len(ioStatement)-2] + "\n"
    fpsv.write(ioStatement)

def generate_sv_file(fppv, fpsv, design, PyComments=False):
    if "/" in (design):
        #print(design.split("/"))
        design = design.split("/")[-1]
    mydesign = importlib.import_module(design)
    thing = getattr(mydesign, design)
    designObj = thing()
    print(designObj.design)
    designObj.exec()
    embKeys = designObj.embStr.keys()
    addInOutStart = False
    addInOutEnd = False
    waitForBracket = False
    inOutSpacing = 0
    pyCodeRegion = False
    lineNum = 0
    for line in fppv:
        if not addInOutStart:
            fpsv.write(line)
            if waitForBracket:
                match = re.search(r"(\()+\;", line)
                if (match):
                    addInOutStart = True
                    printInOutSigns(fpsv, designObj, inOutSpacing)
            match = re.search(r"module\s+([A-Za-z0-9]+)\s*(\#?)(\(?)", line)
            if (match):
                inOutSpacing = len(line) - 1
                print(match.groups())
                if (match.groups()[1]):
                    waitForBracket = True
                elif not (match.groups()[2]):
                    waitForBracket = True
                else:
                    waitForBracket = False
                    addInOutStart = True
                    printInOutSigns(fpsv, designObj, inOutSpacing)
        elif not addInOutEnd:
            match = re.search(r"(\))+\s*\;", line)
            if (match):
                addInOutEnd = True
                fpsv.write(");\n")
                printWireSigns(fpsv, designObj)
        else:
            match = re.search(r"(\<\!)", line)
            if (match):
                pyCodeRegion = True
                if PyComments:
                    wrStr = "// " + line
                    fpsv.write(wrStr)
            if not (pyCodeRegion):
                fpsv.write(line)
            else:
                if str(lineNum) in (embKeys):
                    fpsv.write(designObj.embStr[str(lineNum)])
                    #print("Found embedded string")
            match = re.search(r"(\!\>)",line)
            if (match):
                pyCodeRegion = False
                if PyComments:
                    wrStr = "// " + line
                    fppy.write(wrStr)
        lineNum = lineNum + 1

def create_verilog_from_python():
    parser = init_argparse()
    args = parser.parse_args()
    if not args.files:
        print("list of files to parse")
        exit(1)
    print("args.verilog ", args.python)
    for file in args.files:
        print(file)
        fppv = open(file, 'r')
        fileps = file.split(".")
        filepy = fileps[0] + ".py"
        fppy = open(filepy, 'r')
        filesv = fileps[0] + ".sv"
        fpsv = open(filesv, 'w')
        generate_sv_file(fppv, fpsv, fileps[0], args.python)

if __name__ == '__main__':
    create_verilog_from_python()
