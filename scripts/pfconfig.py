import os

class PFConfig:
    def __init__(self,fname="tmp.txt"):
        self.pflibpath = '/home/ldmx/pflib/pflib/'
        self.fname = fname # file name
        self.pc = [] # pf tool commands

    def run(self,run=False):
        with open(self.fname,"w") as fparam:
            for command in self.fcommands:
                fparam.write(f"{command}\n")
            fparam.write("EXIT\n")
            fparam.close()
        if run:
            os.system(f'{self.pflibpath} -s {self.fname}.txt')

    def fc_reset(self):
        self.pc.extend(["FAST_CONTROL","FC_RESET","QUIT"])

    def fc_multisample(self,nsamples):
        self.pc.append("FAST_CONTROL")
        self.pc.append("MULTISAMPLE")
        self.pc.append("Y") # Enable multisample readout? Y/N
        self.pc.append(f"{nsamples}") # Number of samples
        self.pc.append("QUIT")

    def fc_calib(self,l1a_offset):
        self.pc.append("FAST_CONTROL")
        self.pc.append("CALIB") # Setup calibration pulse
        self.pc.append("2") # Calibration pulse length?
        self.pc.append(f"{l1a_offset}") # L1A offset
        self.pc.append("QUIT")

    def roc_resyncload(self,rocs):
        self.pc.append("ROC")
        for iroc in rocs:
            self.pc.extend(["IROC",iroc,"HARDRESET","RESYNCLOAD"])
        self.pc.append("QUIT")

    def roc_loadparam(self,config):
        self.pc.append("ROC") # ROC Configuration
        for iroc in rocs: # IROC: Which ROC to manage?
            self.pc.extend(["IROC",iroc,"LOAD_PARAM",config])
            self.pc.append("N") # Update all parameter values on the chip using the defaults in the manual for any values not provided?
        self.pc.append("QUIT")

    def roc_param(self,register,param,value):
        self.pc.append("ROC")
        self.pc.append("POKE_PARAM") # Change a single parameter value
        self.pc.append(register) # Page
        self.pc.append(param) # Parameter
        self.pc.append(value) # Value
        
    def bias_init(self,board):
        self.pc.append("BIAS") # BIAS voltage setting
        self.pc.append("INIT") # Initialize a board
        self.pc.append(f"{board}") # Board
        self.pc.append("QUIT")

    def bias_set(self,board,hdmi,sipm_led,bias):
        self.pc.append("BIAS")
        self.pc.append("SET") # Set a specific bias line setting
        self.pc.append(f"{board}") # Which board
        self.pc.append(f"{sipm_led}") # SiPM(0) or LED(1) 
        self.pc.append(f"{hdmi}") # Which HDMI connector
        self.pc.append(f"{bias}") # LED BIAS DAC
        
    def elinks_reset(self):
        self.pc.extend(["ELINKS","HARD_RESET","QUIT"])

    def elinks_relink(self):
        self.pc.extend(["ELINKS","RELINK","QUIT"])

    def daq_reset(self):
        self.pc.extend(["DAQ","HARD_RESET","QUIT"])

    def daq_pedestal(self):
        self.pc.extend(["DAQ","PEDESTAL"])
        
    def daq_enable(self,board):
        self.pc.append("DAQ")
        self.pc.append("SETUP") # Setup the DAQ
        self.pc.append("STANDARD") # Do the standard setup for HCAL
        self.pc.append(f"{board}") # FPGA id
        self.pc.append("ENABLE") # Toggle enable status
        self.pc.append("QUIT")
        self.pc.append("QUIT")

    def set_general(self,board=0,rocs=[0,1,2],config="config/march26_1400_LowBiasLEDFlash.raw"):
        self.pc = []
        self.fc_reset()
        self.roc_resyncload(rocs)
        self.elinks_reset()
        self.fc_multisample(7)
        self.roc_loadparam(config)
        self.daq_enable(board)
        self.elinks_relink()

    #def set_charge_injection(self):

    def set_led(self,board=0,hdmi=0,sipm_bias=3784,led_bias=2500):
        self.pc = [] # Should we re-start the commands here?
        self.bias_init(board)
        self.bias_set(board,hdmi,0,sipm_bias)
        self.bias_set(board,hdmi,1,led_bias)

