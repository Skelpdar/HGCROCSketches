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
            fparam.write("exit\n")
            fparam.close()
        if run:
            os.system(f'{self.pflibpath} -s {self.fname}.txt')

    def reset_fc(self):
        self.pc.extend(["FAST_CONTROL","FC_RESET","QUIT"])

    def resync_load(self,rocs):
        self.pc.append("ROC")
        for iroc in rocs:
            self.pc.extend(["iroc",iroc,"HARDRESET","RESYNCLOAD"])
        self.pc.append("quit")
        
    def set_general(self):
        self.pc = []
        self.reset_fc()
        self.resync_load()
        
    def set_led(self,board=0,hdmi=0,sipm_bias=3784,led_bias=2500):
        # self.pc = [] # Should we re-start the commands here?
        self.pc.append("bias") # BIAS voltage setting
        self.pc.append("init") # Initialize a board             
        self.pc.append(f"{board}") # Which board
        
        self.pc.append("set") # Set a specific bias line setting
        self.pc.append(f"{board}") # Which board
        self.pc.append("0") # Set SiPM. SiPM(0) or LED(1)
        self.pc.append(f"{hdmi}") # Which HDMI connector
        self.pc.append(f"{sipm_bias}") # digital to analog SiPM BIAS
        
        self.pc.append("set") # Set a specific bias line setting
        self.pc.append(f"{board}") # Which board
        self.pc.append("1") # Set LED
        self.pc.append(f"{hdmi}") # Which HDMI connector
        self.pc.append(f"{led_bias}") # LED BIAS DAC

        self.pc.append("quit")
        
