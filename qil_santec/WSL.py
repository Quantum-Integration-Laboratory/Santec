from . import santec_usb
import numpy as np
#import santec_usb



class WSL_COMMANDS:
    def _callQueryDecorator(func):
        """
        Workhorse function such that each individual function can return its VISA signature
        and this will handle the whether to query or write

        Command syntax should be 
        def function(self,val:type=None):
            val=valOperation(A,B,func)
            return "Command string",val,bounds

        """
        def callQuery(self,*args,**kwargs):
            command,val,bounds=func(self,*args,**kwargs)
            if val!=None:
                boundCheck(val,bounds)
                val=str(val)
                self.instrument.write(command+' '+val)
            return self.instrument.query(command+"?")
        return callQuery

    @_callQueryDecorator
    def power(self,pow:float=None):
        """
        Sets the lasers power in dBm
        """
        return "POW",pow,(7.0,15.5)
    
    @_callQueryDecorator
    def wavelength(self,wav:float=None):
        "Sets the lasers wavelength in nm, rounded to the neareast 0.001nm"
        wav=valOperation(wav,1E-9,0.001E-9)
        return "WAV",wav,(1527.60E-9,1565.50E-9)
    
    @_callQueryDecorator
    def frequency(self,freq:float=None):
        """
        Sets the lasers frequency in THz,rounded to the neareast 0.0001THz
        """
        freq=valOperation(freq,1E+12,0.0001E12)
        return "FREQ",freq,(191.5E12,196.25E12)
    @_callQueryDecorator
    def offset(self,freq:float=None):
        """
        Sets the lasers finetune frequency in GHz
        Resolution: 0.1GHz 
        """
        freq=valOperation(freq,1E+9,0.1E-9)
        return "FTUN",freq,(-12E9,12E9)
    @_callQueryDecorator    
    def auto(self,val:bool=None):
        """
        Enable or disable auto mode
        """
        return "AUT",val, (0,1)
    @_callQueryDecorator
    def enable(self,val:bool=None):
        """
        Enable or Disable the laser
        """
        return "POW:STAT",val,(0,1)

    @_callQueryDecorator
    def coherentControl(self,val:bool=None):
        """
        Enable or Disable the Coherent Control
        """
        return "COHC",val,(0,1)
    @_callQueryDecorator
    def linewidth(self,val:bool=None):
        """
        Set coherent control linewidth
        """
        freq=valOperation(freq,1E+9,0.1)

        return "FM",val,(0.1,1)

def boundCheck(val,bounds):
    if val<bounds[0] or val>bounds[1]:
        raise ValueError("Value out of range should be between %s & %s"%bounds)

def valOperation(A:float,B:float,res:float,operation=np.multiply):
    """
    Perform an operation(A,B) with a check for None type, and rounds to the specified resolution
    Parameters
    ----------
    A : float
        First Val, this is checked for None type 
    B: float
        Second Val
    res:float
        rounds the result to the nearest multpile of this value
    Operation : func 
        the function to perform

    Returns
    -------
    path : string 
        the path with date information

    """
    if type(A)==type(None):
        return A
    else:
        return round_nearest(operation(A,B),res)
    

def round_nearest(x, a):
    return round(x / a) * a


class WSL_USB(santec_usb.USB_COMMS,WSL_COMMANDS):
    def __init__(self, serialNumber):
        super().__init__(serialNumber)

class WSL_GPIB(santec_usb.USB_COMMS,WSL_COMMANDS):
    def __init__(self, Address):
        raise NotImplementedError("GPIB communication not yet implemented")
        #super().__init__(serialNumber)
