from pfconfig import PFConfig

p = PFConfig("bias.txt")
p.set_led(board=0,hdmi=0,sipm_bias=3784,led_bias=2500)
p.run()
