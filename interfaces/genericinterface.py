from LogicDeclaration import *

class genericinterface:
    def __init__(self, iname='genericinterface'):
        self.name = iname
        self.params = {}
        self.inputs = []
        self.outputs = []
        self.signals = []
        self.configdone = False
        self.clock = self.name + "_clk"
        self.reset = self.name + "_rstn"

    def configure(self):
        print("Running configure")
        self.configdone = True
        for sig,width,direct,comment in (self.signals):
            #print(sig,width,direct,comment)
            if (direct == 'input'):
                self.inputs.append((sig,width))
            elif (direct == 'output'):
                self.outputs.append((sig,width))

    def getIO(self):
        #print("getio-super ", self.configdone)
        iolist = {}
        iolist['inputs'] = self.inputs
        iolist['outputs'] = self.outputs
        return iolist        

    def getConnections(self):
        connectIn = []
        connectOut = []
        paramKeys = self.params.keys()
        for sig,width,direct,comment in (self.signals):
            if (isinstance(width, int)):
                retWidth = ('0', str((width - 1)))
                #print(sig, " ", retWidth)
            elif width in (paramKeys):
                if (self.params[width] > 0):
                    retWidth = ('0', str((self.params[width] - 1)))
                else:
                    retWidth = None
            else:
                retWidth = None
                #print("sig ", sig, " width ", width)
            if (direct == 'input'):
                connectIn.append((sig, retWidth))
            elif (direct == 'output'):
                connectOut.append((sig, retWidth))
        iolist = {}
        iolist['inputs'] = connectIn
        iolist['outputs'] = connectOut
        return iolist        
