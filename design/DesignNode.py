from LogicDeclaration import *
from InterfaceDeclaration import *

class DesignNode:

    def __init__(self, design, modName = None, clock='clk',reset='rstn'):
        self.modName = modName
        self.design = design
        #default clock / reset
        self.clock=clock
        self.reset=reset
        self.params = {}
        self.inputs = []
        self.outputs =  []
        self.wires = []
        self.regs = []
        self.logic = []
        self.useLogic = False
        self.intf = {}
        self.ports = []
        self.instances = []
        self.configDone = False
        self.siglist = []
        self.embStr = {}
        
    def addPort(self, portName, portWidth, portType):
        self.ports.append((portName, portWidth, portType))

    def addIntf(self, intf, name):
        self.intf[name] = intf
        print(intf.clock)
        self.siglist.append((intf.clock, 'clock', None))
        self.siglist.append((intf.reset, 'reset', None))
        for sig,width,direct,comment in (intf.signals):
            if ((direct == 'input') and (intf.mode == 'target')) or ((direct == 'output') and (intf.mode == 'initiator')):
                self.siglist.append((sig, 'input', name))
            else:
                self.siglist.append((sig, 'output', name))
        #print(self.siglist)
                
    def configure(self):
        self.configDone = True
        #for name, width, ttype in (self.ports):

    def addInstance(self, inst, instName):
        self.instances.append((inst, instName))
        
