from .WSL import WSL_COMMANDS,WSL_USB
from qil_Networked.TCP_instrument import cTCPInstrumentServerMixin,cTCPInstrumentClientMixin,functionDecorator
import numpy as np

newPiName = "qil-zumba"
piPort = 1001 # tbd

class FUNCDEFS:
    def __init__(self):
        print("Importing WSL_100 Functions")
        self.lqueries = {
            "AUT": self.auto,
            "POW:STAT": self.enable,
            "COHC": self.coherentControl,
            "FM": self.linewidth
        }

        self.lfunctions = {
            "POW": self.power,
            "WAV": self.wavelength,
            "FREQ": self.frequency,
            "FTUN": self.offset,
        }

class cWSLServer(WSL_USB,cTCPInstrumentServerMixin,FUNCDEFS):
    def __init__(self,host=None,sPort=piPort,silent=False):
        serialNumber = 16120001 # Based off example_usage.ipynb
        WSL_USB.__init__(self,serialNumber) # need to get serialNumber?
        FUNCDEFS.__init__(self)
        cTCPInstrumentServerMixin.__init__(self,host,sPort,silent)

        self.setQueries(self.lqueries)
        self.setFunctions(self.lfunctions)

class cWSLClient(WSL_COMMANDS,cTCPInstrumentClientMixin,FUNCDEFS):
    def __init__(self,**kwargs):
        defkwargs={"host":newPiName,"port":piPort,"bufferSize":1024,"timeout":120}
        kwargs={**defkwargs,**kwargs}
        #CoBrite.__init__(self,init=False)
        FUNCDEFS.__init__(self)
        cTCPInstrumentClientMixin.__init__(self,**kwargs)
        self.setQueries(self.lqueries)
        self.setFunctions(self.lfunctions)

# unsure about lquery/lfunction assignments
# unsure about WSL class used for server and client