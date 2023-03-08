from LogicDeclaration import *
from InterfaceDeclaration import *
import importlib

class DesignNode:

    def __init__(self, design, modName = None, clock=None,reset=None):
        self.modName = modName
        self.design = design
        #default clock / reset
        self.clock=clock
        self.reset=reset
        self.params = {}
        self.inputs = []
        self.outputs =  []
        self.wires = {}
        self.regs = []
        self.logic = []
        self.useLogic = False
        self.intf = {}
        self.ports = []
        self.instances = {}
        self.configDone = False
        self.siglist = []
        self.embStr = {}
        self.intfConnections = {}
        self.portConnections = {}

    def addPort(self, portName, portWidth, portType):
        self.ports.append((portName, portWidth, portType))

    def addIntf(self, intf, fromName, toName = None ):
        self.intf[fromName] = intf
        #print("Clock coming in = ", intf.clock)
        self.siglist.append((intf.clock, 'clock', None))
        self.siglist.append((intf.reset, 'reset', None))
        if (toName):
            inpName = toName + "_" + fromName
            outName = fromName + "_" + toName
        else:
            inpName = fromName
            outName = fromName
        for sig,width,direct,comment in (intf.signals):
            if ((direct == 'input') and (intf.mode == 'target')) or ((direct == 'output') and (intf.mode == 'initiator')):
                self.siglist.append((sig, 'input', inpName))
            else:
                self.siglist.append((sig, 'output', outName))
        #print(self.siglist)
                
    def configure(self):
        self.configDone = True
        if (self.clock):
            self.siglist.append((self.clock, 'clock', None))
        if (self.reset):
            self.siglist.append((self.reset, 'reset', None))
        #self.siglist.append((sig, 'input', name))
        #for name, width, ttype in (self.ports):

    def addInstance(self, inst, instName, portDict=None):
        self.instances[instName] = inst
        mydesign = importlib.import_module(inst)
        thing = getattr(mydesign, inst)
        designObj = thing()
        paramKeys = designObj.params.keys()
        prtKeys = []
        if (portDict):
            prtKeys = portDict.keys()
        for inps, inwidth in (designObj.inputs + designObj.outputs):
            if inps in (prtKeys):
                connectSigName = portDict[inps]
                self.portConnections[inps] = connectSigName
            else:
                connectSigName = instName + "_" + inps
                self.portConnections[inps] = connectSigName
                if (inwidth):
                    if (isinstance(inwidth, int)):
                        rWidth = ('0', str((width - 1)))
                    else :
                        #print(inwidth)
                        rWidth = (0,0)
                        for prms in (paramKeys):
                            if prms in (inwidth):
                                #print("Width param = ", prms)
                                if (isinstance(designObj.params[prms], int)):
                                    rWidth = ('0', str((designObj.params[prms] - 1)))
                else:
                    rWidth = inwidth
                self.wires[connectSigName] = rWidth

    def connectinterfaces(self, intf1, intf2):
        self.intfConnections[intf1] = intf2
        self.intfConnections[intf2] = intf1

    def connectports(self, port1, port2):
        self.portConnections[port1] = port2

    def createInstance(self, inst):
        instansStr = '//No such instance'
        instansStrSize = 1
        connKeyList = self.intfConnections.keys()
        #print(connKeyList)
        if (self.instances[inst]):
            instansStr = self.instances[inst] + " " + inst + "(\n"
            instansStrSize = len(instansStr) - 1
            spaceStr = ''
            for ns in range(instansStrSize):
                spaceStr = spaceStr + ' '

            #print(self.instances[inst])
            mydesign = importlib.import_module(self.instances[inst])
            thing = getattr(mydesign, self.instances[inst])
            designObj = thing()
            if callable(getattr(designObj, 'exec', None)):
                designObj.exec()
            #print(designObj.intf)
            intfsList = designObj.intf.keys()
            #print(intfsList)
            for infs in (intfsList):
                conStr = inst + "." + infs
                #print(conStr)
                curIntf = designObj.intf[infs]
                #print("Name = ", curIntf.name, " clock = ", curIntf.clock)
                sigStr = curIntf.clock
                instansStr = instansStr + spaceStr + "." + sigStr + "( " + sigStr + " ),\n"
                sigStr = curIntf.reset
                instansStr = instansStr + spaceStr + "." + sigStr + "( " + sigStr + " ),\n"
                if conStr in connKeyList:
                    #print("Have connect to ", self.intfConnections[conStr])
                    #print("Mode setting ", curIntf.mode)
                    iolist = curIntf.getConnections()
                    inputs = iolist['inputs']
                    inpSigList = inputs.keys()
                    #print(inpSigList)
                    otherIntfs = self.intfConnections[conStr].split(".")[1]

                    for inpSigs in (inpSigList):
                        sigStr = infs + "_" + inpSigs
                        conStr = otherIntfs + "_" + infs + "_" + inpSigs
                        instansStr = instansStr + spaceStr + "." + sigStr + "( " + conStr + " ),\n"
                        self.wires[conStr] = inputs[inpSigs]
                    outputs = iolist['outputs']
                    outSigList = outputs.keys()
                    for outSigs in (outSigList):
                        sigStr = infs + "_" + outSigs
                        conStr = infs + "_" + otherIntfs + "_" + outSigs
                        #print(conStr)
                        instansStr = instansStr + spaceStr + "." + sigStr + "( " + conStr + " ),\n"
                        self.wires[conStr] = outputs[outSigs]
                else:
                    iolist = curIntf.getConnections()
                    inputs = iolist['inputs']
                    inpSigList = inputs.keys()
                    #print(inpSigList)
                    for inpSigs in (inpSigList):
                        sigStr = infs + "_" + inpSigs
                        instansStr = instansStr + spaceStr + "." + sigStr + "( " + sigStr + " ),\n"
                        #self.wires[sigStr] = inputs[inpSigs]
                        self.siglist.append((sigStr, 'int_input', inputs[inpSigs]))
                    outputs = iolist['outputs']
                    outSigList = outputs.keys()
                    for outSigs in (outSigList):
                        sigStr = infs + "_" + outSigs
                        instansStr = instansStr + spaceStr + "." + sigStr + "( " + sigStr + " ),\n"
                        #self.wires[sigStr] = outputs[outSigs]
                        self.siglist.append((sigStr, 'int_output', outputs[outSigs]))
            portKeys = self.portConnections.keys()
            connectedPorts = {}
            for prts in (portKeys):
                #print("portKeys - ", prts)
                if "\." in (prts):
                    print("portKeys - ", prts)
                    frmPort = prts.split(".")[1]
                    connectedPorts[frmPort] = self.portConnections[prts]
                else:
                    frmPort = prts
                toPorts = self.portConnections[prts]
                if "\." in (prts):
                    print(toPorts)
                    toPorts = toPorts.split(".")[1]
                instansStr = instansStr + spaceStr + "." + frmPort + "( " + toPorts + " ),\n"
                #self.siglist.append((frmPort, 'int_input', toPorts))
            cportKeys = connectedPorts.keys()
            for inps, inwidth in (designObj.inputs + designObj.outputs):
                if (inps) not in (portKeys) and (inps) not in (cportKeys):
                    if inps in (connKeyList):
                        instansStr = instansStr + spaceStr + "." + inps + "( " + self.intfConnections[inps] + " ),\n"
                    else:
                        instansStr = instansStr + spaceStr + "." + inps + "( " + "   "  + " ),\n"
            instansStr = instansStr[0:len(instansStr)-2] + "\n" + spaceStr + ");\n"
        #print(instansStr)
        return instansStr
