import santec_usb


class WSL_USB(santec_usb.USB_COMMS):
    def __init__(self, serialNumber=16120001):
        super().__init__(serialNumber)

    def _callQueryDecorator(func):
        """
        Workhorse function such that each individual function can return its VISA signature
        and this will handle the whether to query or write

        """
        def callQuery(self,*args,**kwargs):
            command=func
            val=kwargs["val"]
            if val!=None:
                self.instrument.write(command+' '+val)
            return self.instrument.query(command)
        return callQuery

    @_callQueryDecorator
    def power(self,val=None):
        return "POW"