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
        #self.pflibpath = f'/home/ldmx/pflib/pflib_jm/pftool {dpm}'
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

    def __call__(self, *args) :
        for a in args :
            if isinstance(a,list) :
                self(*a)
            else :
                self._file.write(f'{a}\n')
        self._file.flush()

    def run(self,run=False):
        if run :
            subprocess.run(f'{self.pflibpath} -s {self._file.name}',shell=True,check=True)
        else :
            print(str(self))

    def fc_reset(self):
        self("FAST_CONTROL","FC_RESET","QUIT")

    def fc_multisample(self,nsamples):
        self("FAST_CONTROL")
        self("MULTISAMPLE")
        self("Y") # Enable multisample readout? Y/N
        self(nsamples) # Number of samples
        self("QUIT")

    def fc_calib(self,l1a_offset):
        self("FAST_CONTROL")
        self("CALIB") # Setup calibration pulse
        self("2") # Calibration pulse length?
        self(l1a_offset) # L1A offset
        self("QUIT")

    def roc_resyncload(self,rocs):
        self("ROC")
        for iroc in rocs:
            self("IROC",iroc,"HARDRESET","RESYNCLOAD")
        self("QUIT")

    def roc_loadparam(self,config,rocs):
        self("ROC") # ROC Configuration
        for iroc in rocs: #rocs: # IROC: Which ROC to manage?
            self("IROC",iroc,"LOAD_PARAM",config)
            self("N") # Update all parameter values on the chip using the defaults in the manual for any values not provided?
        self("QUIT")
        
    def roc_param(self,register,param,value,rocs):
        self("ROC")
        for iroc in rocs:
            self("POKE_PARAM") # Change a single parameter value
            self(register) # Page
            self(param) # Parameter
            self(value) # Value
        self("QUIT")

    def bias_init(self,board):
        self("BIAS") # BIAS voltage setting
        self("INIT") # Initialize a board
        self(f"{board}") # Board
        self("QUIT")

    def bias_set(self,board,hdmi,sipm_led,bias):
        self("BIAS")
        self("SET") # Set a specific bias line setting
        self(board) # Which board
        self(sipm_led) # SiPM(0) or LED(1) 
        self(hdmi) # Which HDMI connector
        self(bias) # LED BIAS DAC
        self("QUIT")

    def elinks_reset(self):
        self("ELINKS","HARD_RESET","QUIT")

    def elinks_relink(self):
        self("ELINKS","RELINK","QUIT")

    def daq_reset(self):
        self("DAQ","HARD_RESET","QUIT")

    def daq_pedestal(self,nevents=100,output_name="100.raw"):
        self("DAQ","PEDESTAL",nevents,output_name,"QUIT")
        
    def daq_charge(self,nevents=100,output_name="100.raw"):
        self("DAQ","CHARGE",nevents,output_name,"QUIT")

    def daq_enable(self,board):
        self("DAQ")
        self("SETUP") # Setup the DAQ
        self("STANDARD") # Do the standard setup for HCAL
        self(board) # FPGA id
        self("ENABLE") # Toggle enable status
        self("QUIT")
        self("QUIT")

    def set_general(self,board=0,rocs=[0,1,2],config="configs/march26_1400_LowBiasLEDFlash.raw",l1a_offset=17):
        self.fc_reset()
        self.roc_resyncload(rocs)
        self.elinks_reset()
        self.daq_reset()
        self.fc_multisample(3)
        self.roc_loadparam(config,rocs)
        self.fc_calib(l1a_offset)
        self.bias_init(board)
        self.daq_enable(board)
        self.elinks_relink()

    def set_charge_injection(self,off=False,rocs=[0]):
        if off:
            self.roc_param("Reference_Voltage_0","Calib_dac",0,rocs)
            self.roc_param("Reference_Voltage_0","IntCtest",0,rocs)
            self.roc_param("Channel_0","HighRange",0,rocs)
        else:
            self.roc_param("Reference_Voltage_0","Calib_dac",50,rocs)
            self.roc_param("Reference_Voltage_0","IntCtest",1,rocs)
            self.roc_param("Channel_0","HighRange",1,rocs)

    def set_led(self,board=0,hdmi=0,sipm_bias=3784,led_bias=2500):
        self.bias_init(board)
        self.bias_set(board,hdmi,0,sipm_bias)
        self.bias_set(board,hdmi,1,led_bias)

    def set_bias(self,board=0,hdmi=0,sipm_bias=3784):
        self.bias_init(board)
        self.bias_set(board,hdmi,0,sipm_bias)        

def connect(dpm):
    return PFConfig(dpm)
