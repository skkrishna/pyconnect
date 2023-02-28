from LogicDeclaration import *
from genericinterface import *

class axiinterface(genericinterface):
    def __init__(self, mode='target', params=None, rev=4):
        super().__init__('axiinterface')
        self.mode = mode
        self.rev = rev
        self.clock = 'aclk'
        self.reset = "arstn"
        self.params['WIDWIDTH'] = 2
        self.params['ADDRWIDTH'] = 32
        self.params['BURSTLEN'] = 3
        self.params['WUSRWIDTH'] = 0
        self.params['WDATAWIDTH'] = 64
        self.params['WSTRBWIDTH'] = 8
        self.params['RIDWIDTH'] = 2
        self.params['RUSRWIDTH'] = 0
        self.params['RDATAWIDTH'] = 64

        self.signals = [('awid',	'WIDWIDTH',  'input',	"Write address ID. This signal is the ID tag for the write address group of signals."),
                        ('awaddr',	'ADDRWIDTH', 'input',	"Write address. The write address gives the address of the first transfer in a write burst transaction."),
                        ('awlen',	'BURSTLEN',  'input',   "Burst Length. The burst length gives the exact number of transfers in a burst. This information determines the number of data transfers associated with the address."),
                        ('awsize',	3,	     'input',	"Burst Size. This signal indicates the size of each transfer in the burst."),
                        ('awburst',	2,	     'input',	"The burst type and the size information, determined how the address for each transfer within the burst is calculated. 2b01	INCR"),
                        ('awprot',	3,	     'input',	"Protection Type. 3b000 = No protection"),
                        ('awqos',	4,	     'input',	"Quality of Service. The Quality of Service identifier sent for each write transaction. 4b1111 = High priority 4b0000 = Normal priority"),
                        ('awuser',	'WUSRWIDTH', 'input',	"User Signal"),
                        ('awvalid',	None,	  'input',	"Write Address Valid. Indicates that the channel is signaling valid write address and control information."),
                        ('awready',	None,	  'output', "Write Address Ready. Indicates that the slave is ready to accept an address and associated control signals."),
                        #AXI4 Write Data Channel
                        ('wdata',	'WDATAWIDTH', 'input', "Write Data."),
                        ('wstrb',	'WSTRBWIDTH', 'input', "Write Strobes (Byte Enables). Indicates which byte lanes hold valid data."),
                        ('wlast',	None,	'input',	"Write Last. Indicates the last transfer in a write burst."),
                        ('wvalid',	None,	'input',	"Write Valid. Indicates that valid write data and strobes are valid."),
                        ('wready',	None,	'output',	"Write Ready. Indicates that the slave (HBM2 controller) can accept write data."),
                        #Write Response Channel
                        ('bid',	'WIDWIDTH', 'output',	"Response ID Tag. The ID tag of the write response."),
                        ('bresp',	2,	'output',	"Write response. Indicates the status of the write transaction. 2b00 = OKAY"),
                        ('bvalid',	None,	'output',	"Write response valid. Indicates that the channel is signaling a valid write response."),
                        ('bready',	None,	'input',	"Response ready. Indicates that the master can accept a write response."),
                        #AXI4 Read Address (Command) Channel
                        ('arid',	'RIDWIDTH', 'input',	"Read address ID. The ID tag for the read address group of signals."),
                        ('araddr',	'ADDRWIDTH', 'input',	"Read address. The address of the first transfer in a read burst transaction."),
                        ('arlen',	'BURSTLEN', 'input',	"Burst Length. The burst length gives the exact number of transfers in a burst."),
                        ('arsize',	3,	'input',	"Burst Size. This signal indicates the size of each transfer in the burst."),
                        ('arburst',	2,	'input',	"The burst type and the size information, determined how the address for each transfer within the burst is calculated. 2b01	INCR"),
                        ('arprot',	3,	'input',	"Protection Type. [Reserved for Future Use] Indicates the privilege and security level of the transaction, and whether the transaction is a data access or an instruction access. 3b000 = No protection"),
                        ('arqos',	4,	'input',	"Quality of Service. The Quality of Service identifier sent for each write transaction."),
                        ('aruser',	'RUSRWIDTH', 'input',	"User Signal"),
                        ('arvalid',	None,	'input',	"Read address valid. Indicates that the channel signals valid read address and control information."),
                        ('arready',	None,	'output',	"Read address ready. Indicates that the slave is ready to accept an address and associated control signals."),
                        #Read response
                        ('rid',	 'RIDWIDTH', 'output',	"Read ID tag. The ID tag for the read data group of signals generated by the slave."),
                        ('rdata',	'RDATAWIDTH', 'output',       "Read data."),
                        ('rresp',	2,	'output',	"Read response. Indicates the status of the read transfer: 2b00 = OKAY"),
                        ('rlast',	None,	'output',	"Read last. Indicates the last transfer in a read burst."),
                        ('rvalid',	None,	'output',	"Read valid. Indicates that the channel is signaling the required read data."),
                        ('rready',	None,	'input',	"Read ready. Indicates that the master can accept the read data and response information.")]

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
            


        
