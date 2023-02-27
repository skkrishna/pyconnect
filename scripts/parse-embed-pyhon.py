import sys
import re
import argparse

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Generate Python file from embedded verilog file .pv -> .py"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('files', nargs='*')
    parser.add_argument("--verilog", help="Keep commented verilog code",
                    action="store_true")
    return parser

def printPyInit(fppy,sigDict,params=None,spaceStr="\t"):
    initStr = spaceStr + "def __init__(self):\n"
    fppy.write(initStr)
    spaceStr = spaceStr + "\t"
    lstStr = spaceStr + "super().__init__('"+ sigDict['design'] + "')\n"
    fppy.write(lstStr)
    if (sigDict['inputs']):
        lstStr = "self.inputs = [  "
        for sig in (sigDict['inputs']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)
    if (sigDict['outputs']):
        lstStr = "self.outputs = [  "
        for sig in (sigDict['outputs']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)
    if (sigDict['wires']):
        lstStr = "self.wires = [  "
        for sig in (sigDict['wires']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)
    if (sigDict['regs']):
        lstStr = "self.regs = [  "
        for sig in (sigDict['regs']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)
    if (sigDict['logic']):
        lstStr = "self.logic = [  "
        for sig in (sigDict['logic']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)
    #Keep the siglist to rememer the order of signals
    if (sigDict['siglist']):
        lstStr = "self.siglist = [  "
        for sig in (sigDict['siglist']):
            lstStr = lstStr + str(sig) + ", "
        lstStr = spaceStr+lstStr[0:(len(lstStr)-2)] + "]\n"
        fppy.write(lstStr)

def generate_py_file(fppv, fppy, design, VerComments=False):
    modN = False
    inputs = []
    outputs = []
    wires = []
    regs = []
    logic = []
    siglist = []
    params = {}
    modSigs = {}
    pyCodeRegion = False
    lineNum = 0
    pyCodeStart = False
    fppy.write("from LogicDeclaration import *\n")
    fppy.write("from InterfaceDeclaration import *\n")
    fppy.write("from DesignNode import *\n\n")
    spaceStr = "\t"
    for line in fppv:
        match = re.search(r"module\s+([A-Za-z0-9]+)\s*[\#\(]?", line)
        if (match):
            print(match)
            modN = True
            modName = match.group(1)
            print("Module = ", modName)
            inputs = []
            outputs = []
            wires = []
            regs = []
            logic = []
            siglist = []
        match = re.search(r"input\s+(logic )?(wire )?\[\s*([A-Za-z0-9\:\s\`]+)\]\s+([A-Za-z0-9]+)", line)
        if (match):
            print(match)
            inputs.append((match.group(4), match.group(3)))
            siglist.append((match.group(4), 'inputs'))
            print(match.group(3))
            print(match.group(4))
        match = re.search(r"input\s+(logic )?(wire )?\s*([A-Za-z0-9]+)", line)
        if (match):
            print(match)
            print(match.group(3))
            inputs.append((match.group(3), None))
            siglist.append((match.group(3), 'inputs'))
        match = re.search(r"output\s+(logic )?(wire )?\[\s*([A-Za-z0-9\:\s\`]+)\]\s+([A-Za-z0-9]+)", line)
        if (match):
            print(match)
            outputs.append((match.group(4), match.group(3)))
            siglist.append((match.group(4), 'outputs'))
            print(match.group(3))
            print(match.group(4))
        match = re.search(r"output\s+(logic )?(wire )?\s*([A-Za-z0-9]+)", line)
        if (match):
            print(match)
            print(match.group(3))
            outputs.append((match.group(3), None))
            siglist.append((match.group(3), 'outputs'))
        match = re.search(r"endmodule", line)
        if (match):
            #print("end module")
            #pyCodeStart = False
            modSigs['inputs'] = inputs
            modSigs['outputs'] = outputs
            modSigs['wires'] = wires
            modSigs['regs'] = regs
            modSigs['logic'] = logic
            modSigs['siglist'] = siglist
            print("pyCodeRegion ", pyCodeRegion)
            print("pyCodeStart ", pyCodeStart)
            if not pyCodeStart:
                if (modN):
                    pyClass = "class " + modName + "(DesignNode):\n"
                    modSigs['design'] = modName
                else:
                    pyClass = "class " + design + "(DesignNode):\n"
                    modSigs['design'] = design
                fppy.write(pyClass)
            printPyInit(fppy,modSigs,params)
            inputs = []
            outputs = []
            wires = []
            regs = []
            params = {}
            pyCodeRegion = False
            pyCodeStart = False
        match = re.search(r"(\<\!)", line)
        if (match):
            pyCodeRegion = True
            wrStr = "## " + line
            if VerComments:
                fppy.write(wrStr)
            continue
        match = re.search(r"(\!\>)",line)
        if (match):
            pyCodeRegion = False
        if not (pyCodeRegion):
            if VerComments:
                wrStr = "## " + line
                fppy.write(wrStr)
        else:
            if not pyCodeStart:
                if (modN):
                    pyClass = "class " + modName + "(DesignNode):\n"
                    modSigs['design'] = modName
                else:
                    pyClass = "class " + design + "(DesignNode):\n"
                    modSigs['design'] = design
                fppy.write(pyClass)
                defStr = "\n\n" + spaceStr + "def exec(self):\n"
                fppy.write(defStr)
                spaceStr = spaceStr + "\t"
                pyCodeStart = True
            match = re.search(r"\!\!", line)
            if (match):
                #print("Found !! = ", line)
                subStr = "self.embStr['" +  str(lineNum) + "'] = self."
                line = re.sub(r"\!\!\s?", subStr, line)
            lineOut = spaceStr + line
            fppy.write(lineOut)
        lineNum = lineNum + 1


def parse_embed_python():
    parser = init_argparse()
    args = parser.parse_args()
    if not args.files:
        print("list of files to parse")
        exit(1)
    print("args.verilog ", args.verilog)
    for file in args.files:
        print(file)
        fppv = open(file, 'r')
        fileps = file.split(".")
        filepy = fileps[0] + ".py"
        fppy = open(filepy, 'w')
        generate_py_file(fppv, fppy, fileps[0], args.verilog)

if __name__ == '__main__':
    parse_embed_python()
