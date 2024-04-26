# qil_santec
A driver to interface with the santec laser, or potentially any santec device
## Installation
In order to make files easier to access they can be installed as a package via pip and such.

Our naming convention for a driver is `qil_<DriverName>` matching cases, where `<>` indicates the parts you can change. 
 
With the driver repo written it should be cloned onto a lab pc using github desktop, into the directory `./Docs/GITHUB/Drivers/`, such that there will now be a folder named `./Docs/GITHUB/Drivers/santec`. with structure
```
<repo name>
  |->qil_santec
  ...
  |->requirements.txt
  \->setup.py
```

With everything cloned correctly, open a terminal or anaconda prompt depending on what is used `cd ./<path>/<repo name>` and then run 
```
pip install --editable .
```
The `--editable` flag means the installed script just points back to the folder so updates will be recognised when we pull any updates into this folder

## Expanding code

### WSL_Commands
The class`WSL_COMMANDS` defines all the functions we want to call, it is currently setup so that that the bulk of the code is handled by the decorator function `@_callQueryDecorator`, this largely handles checking if we have provided a value to any of the commands and sending a query if we have not. Any function that implements a SCPI call to the device should be of the form
```
@_callQueryDecorator
def function(self,val:type=None):
  val=valOperation(val,B,res,func=multiply)
  return "Command string",val,(Lower Bound, Upper Bound)
```
`valOperation` performs some function on A and B after first checking that val is not None, it will then round the result to the nearest value of `res`.
We then return the command string we want to call, this manipulated `val`, and a tuple of the upper and lower bound to check this is a valid call.

`WSL_COMMANDS` currently doesn't define how `query` and `write` are implemented, it is designed to act as a co-parent class with a communications class that will implement them as `instrument.query()` and `instrument.write()`. This is currently implemented for USB (.dll mediated) communications via `qil_santec.santec_usb.USB_COMMS` that is required as the other parent class.

In the future there will also be a class defining GPIB communication.
