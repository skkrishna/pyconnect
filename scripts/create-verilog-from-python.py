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

def printInOutSigns(fpsv, designObj, spaceSize=0):
    spaceStr = ''
    for ns in range(spaceSize):
        spaceStr = spaceStr + ' '

    inpList = {}
    outList = {}
    for sigName, sigTpe, sigIntf in (designObj.siglist):
        if (sigIntf):
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
                sigWidth = outList[sigName]
                if (outList[sigName]):
                    ioLine = spaceStr + 'output logic ' +  "[" + sigWidth[1] + " : " + sigWidth[0] + "] " + sigStr + ",\n"
                else:
                    ioLine = spaceStr + 'output logic ' + sigStr + ",\n"
            else:
                ioLine = spaceStr + 'input logic ' + sigName + ",\n"
            fpsv.write(ioLine)

def generate_sv_file(fppv, fpsv, design, PyComments=False):
    if "/" in (design):
        #print(design.split("/"))
        design = design.split("/")[-1]
    mydesign = importlib.import_module(design)
    thing = getattr(mydesign, design)
    designObj = thing()
    print(designObj.design)
    designObj.exec()
    addInOutStart = False
    addInOutEnd = False
    waitForBracket = False
    inOutSpacing = 0
    pyCodeRegion = False
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
        else:
            match = re.search(r"(\<\!)", line)
            if (match):
                pyCodeRegion = True
                if PyComments:
                    wrStr = "// " + line
                    fppy.write(wrStr)
            if not (pyCodeRegion):
                fpsv.write(line)
            match = re.search(r"(\!\>)",line)
            if (match):
                pyCodeRegion = False
                if PyComments:
                    wrStr = "// " + line
                    fppy.write(wrStr)

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
