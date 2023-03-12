from LogicDeclaration import *
from genericinterface import *

class apbinterface(genericinterface):
    def __init__(self, mode='target', params=None, rev=4):
        super().__init__('apbinterface')
        self.mode = mode
        self.rev = rev
        self.clock = 'pclk'
        self.reset = "prstn"
        self.params['ADDRWIDTH'] = 32
        self.params['DATAWIDTH'] = 32
        self.params['NUMSLAVES'] = 1

        self.signals = [('paddr', 'ADDRWIDTH', 'input', "address bus from master to slave, can be up 32 to bit wide"),
                        ('pwdata', 'DATAWIDTH', 'input', "write data bus from master to slave, can be up to 32 bit wide"),
                        ('prdata', 'DATAWIDTH', 'output', "Read data us from Slave to Master, can be up to 32 bit wide"),
                        ('psel', 'NUMSLAVES', 'input', "Slave select signal, there will be one PSEL signal for each slave connected to master. If master connected to ‘n’ number of slaves, PSELn is the maximum number of signals present in the system. (Eg: PSEL1,PSEL2,..,PSELn)"),
                        ('penable', None, 'input', "Indicates the second and subsequent cycles of transfer. When PENABLE is asserted, the ACCESS phase in the transfer starts."),
                        ('pwrite', None, 'input', "Indicates Write when HIGH, Read when LOW"),
                        ('pready', None,  'output', "It is used by the slave to include wait states in the transfer. i.e. whenever slave is not ready to complete the transaction, it will request the master for some time by de-asserting the PREADY."),
                        ('pslverr', None, 'input', "Indicates the Success or failure of the transfer. HIGH indicates failure and LOW indicates Success")]

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
            


        
