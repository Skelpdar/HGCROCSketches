"""Run a script through pftool

Open the config, list the commands you want to use, then run it.

    import pfconfig
    with pfconfig.open() as c :
        c.set_general()
        c.run()

"""

import tempfile
import subprocess

class PFConfig :
    """PFConfig class which is a special tyep of temporary file
    
    Examples
    --------
    Create it, write commands, run the pftool.

        from pfconfig import PFConfig
        with PFConfig() as c :
            c.set_general()
            c.run()

    Even better, use simpler open function:
        
        import pfconfig
        with pfconfig.open() as c :
            c.set_general()
            c.run()

    """

    def __init__(self,dpm="cob1-dpm0") :
        self._file = tempfile.NamedTemporaryFile(mode='w+')
        self.pflibpath = f'/home/ldmx/pflib/pflib/pftool {dpm}'
        print(f'To run {self.pflibpath}')
        
    def __enter__(self) :
        return self

    def __exit__(self,exc_type, exc_value, exc_traceback) :
        self._file.__exit__(exc_type, exc_value, exc_traceback)

    def __str__(self) :
        with open(self._file.name,'r') as r :
            return r.read()

    def __enter__(self) :
        return self

    def __exit__(self,exc_type, exc_value, exc_traceback) :
        self._file.__exit__(exc_type, exc_value, exc_traceback)

    def __str__(self) :
        with open(self._file.name,'r') as r :
            return r.read()

    def run(self,run=False):
        if run :
            subprocess.run(f'{self.pflibpath} -s {self._file.name}',shell=True,check=True)
        else :
            print(str(self))

    def cmd(self,cmds) :
        if isinstance(cmds,list):
            for c in cmds :
                self._file.write(f'{c}\n')
        else:
            self._file.write(f'{cmds}\n')
        self._file.flush()

    def fc_reset(self):
        self.cmd(["FAST_CONTROL","FC_RESET","QUIT"])

    def fc_multisample(self,nsamples):
        self.cmd("FAST_CONTROL")
        self.cmd("MULTISAMPLE")
        self.cmd("Y") # Enable multisample readout? Y/N
        self.cmd(nsamples) # Number of samples
        self.cmd("QUIT")

    def fc_calib(self,l1a_offset):
        self.cmd("FAST_CONTROL")
        self.cmd("CALIB") # Setup calibration pulse
        self.cmd("2") # Calibration pulse length?
        self.cmd(l1a_offset) # L1A offset
        self.cmd("QUIT")

    def roc_resyncload(self,rocs):
        self.cmd("ROC")
        for iroc in rocs:
            self.cmd(["IROC",iroc,"HARDRESET","RESYNCLOAD"])
        self.cmd("QUIT")

    def roc_loadparam(self,config,rocs):
        self.cmd("ROC") # ROC Configuration
        for iroc in rocs: #rocs: # IROC: Which ROC to manage?
            self.cmd(["IROC",iroc,"LOAD_PARAM",config])
            self.cmd("N") # Update all parameter values on the chip using the defaults in the manual for any values not provided?
        self.cmd("QUIT")

    def roc_param(self,register,param,value):
        self.cmd("ROC")
        self.cmd("POKE_PARAM") # Change a single parameter value
        self.cmd(register) # Page
        self.cmd(param) # Parameter
        self.cmd(value) # Value
        self.cmd("QUIT")

    def bias_init(self,board):
        self.cmd("BIAS") # BIAS voltage setting
        self.cmd("INIT") # Initialize a board
        self.cmd(f"{board}") # Board
        self.cmd("QUIT")

    def bias_set(self,board,hdmi,sipm_led,bias):
        self.cmd("BIAS")
        self.cmd("SET") # Set a specific bias line setting
        self.cmd(board) # Which board
        self.cmd(sipm_led) # SiPM(0) or LED(1)  
        self.cmd(hdmi) # Which HDMI connector
        self.cmd(bias) # LED BIAS DAC
        self.cmd("QUIT")

    def elinks_reset(self):
        self.cmd(["ELINKS","HARD_RESET","QUIT"])

    def elinks_relink(self):
        self.cmd(["ELINKS","RELINK","QUIT"])

    def daq_reset(self):
        self.cmd(["DAQ","HARD_RESET","QUIT"])

    def daq_pedestal(self,nevents=100,output_name="100.raw"):
        self.cmd(["DAQ","PEDESTAL",nevents,output_name,"QUIT"])
        
    def daq_charge(self,nevents=100,output_name="100.raw"):
        self.cmd(["DAQ","CHARGE",nevents,output_name,"QUIT"])

    def daq_enable(self,board):
        self.cmd("DAQ")
        self.cmd("SETUP") # Setup the DAQ
        self.cmd("STANDARD") # Do the standard setup for HCAL
        self.cmd(board) # FPGA id
        self.cmd("ENABLE") # Toggle enable status
        self.cmd("QUIT")
        self.cmd("QUIT")

    def set_general(self,board=0,rocs=[0,1,2],config="configs/march26_1400_LowBiasLEDFlash.raw",l1a_offset=17):
        self.fc_reset()
        self.roc_resyncload(rocs)
        self.elinks_reset()
        self.daq_reset()
        self.fc_multisample(7)
        self.roc_loadparam(config,rocs)
        self.fc_calib(l1a_offset)
        self.bias_init(board)
        self.daq_enable(board)
        self.elinks_relink()
        self.cmd("EXIT")

    def set_charge_injection(self,off=False):
        if off:
            self.roc_param("Reference_Voltage_0","Calib_dac",0)
            self.roc_param("Reference_Voltage_0","IntCtest",0)
            self.roc_param("Channel_0","HighRange",0)
        else:
            self.roc_param("Reference_Voltage_0","Calib_dac",50)
            self.roc_param("Reference_Voltage_0","IntCtest",1)
            self.roc_param("Channel_0","HighRange",1)
        self.cmd("EXIT")

    def set_led(self,board=0,hdmi=0,sipm_bias=3784,led_bias=2500):
        self.bias_init(board)
        self.bias_set(board,hdmi,0,sipm_bias)
        self.bias_set(board,hdmi,1,led_bias)
        self.cmd("EXIT")

    def set_bias(self,board=0,hdmi=0,sipm_bias=3784):
        self.bias_init(board)
        self.bias_set(board,hdmi,0,sipm_bias)

def connect(dpm):
    return PFConfig(dpm)
