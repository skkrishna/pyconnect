from LogicDeclaration import *
from genericinterface import *

class atbinterface(genericinterface):
    def __init__(self, mode='target', params=None, rev=4):
        super().__init__('atbinterface')
        self.mode = mode
        self.rev = rev
        self.clock = 'pclk'
        self.reset = "prstn"
        self.params['IDWIDTH'] = 7
        self.params['DATAWIDTH'] = 32
        self.params['SIZEWIDTH'] = 2

        self.signals = [('atclken', None, 'output', "ATB clock enable"),
                        ('atreadymx', None, 'output', "ATB device ready"),
                        ('afvalidmx', None, 'output', "FIFO flush request"),
                        ('atdatamx', 'DATAWIDTH', 'input', "Data Output"),
                        ('atvalidmx', None, 'input', "Data valid"),
                        ('atbytesmx', 'SIZEWIDTH', 'input', "Data size"),
                        ('afreadymx', None, 'input', "FIFO flush finished"),
                        ('atidmx', 'IDWIDTH', 'input', "Trace source ID"),
                        ('syncreqmx', None, 'output', "Synchronization request from the trace sink")]

    def getIO(self, mode=None):
        #print("getio ", self.configdone)
        if not mode:
            mode = self.mode
        if not (self.configdone):
            super().configure()
        if (mode == self.mode):
            return super().getIO()
        else:
            iolist = super().getIO()
            slist = iolist['inputs']
            iolist['inputs'] = iolist['outputs']
            iolist['outputs'] = slist
            return iolist

    def getConnections(self, mode=None):
        if not mode:
            mode = self.mode
        if not (self.configdone):
            super().configure()
        if (mode == self.mode):
            return super().getConnections()
        else:
            iolist = super().getConnections()
            slist = iolist['inputs']
            iolist['inputs'] = iolist['outputs']
            iolist['outputs'] = slist
            return iolist
            


        
