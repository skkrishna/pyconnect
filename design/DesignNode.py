from LogicDeclaration import *
from InterfaceDeclaration import *
from DesignNode import *

class DesignNode:

    def __init__(self, design, modName = None, clock='clk',reset='rstn'):
        self.modName = modName
        self.design = design
        self.clock=clock
        self.reset=reset
        self.params = {}
        self.inputs = []
        self.outputs =  []
        self.wires = []
        self.regs = []
        self.useLogic = False
        self.intf = []
        self.ports = []
        
        
