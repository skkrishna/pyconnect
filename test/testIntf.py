#from t_mem_fifo import *
#from t_var_pinsizes import *
#from t_array_mda import *
#from t_case_zx_bad import *
#from t_param_no_parentheses import *
#from pad_vdd import *
#from ac_ana import *
from axiinterface import *


def test_embed_python():
    axif = axiinterface()
    print(axif.name)
    iosigs = axif.getIO()
    print( iosigs['inputs'])
    print( iosigs['outputs'])
    iosigs = axif.getConnections('initiator')
    print( iosigs['inputs'])
    print( iosigs['outputs'])

if __name__ == '__main__':
    test_embed_python()
