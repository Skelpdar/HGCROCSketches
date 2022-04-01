import argparse

delay_values = {
    'DELAY40': 2, # 5 in our default config
    'DELAY65': 2,
    'DELAY87': 2,
    'DELAY9': 2,
}

def delay_action(arg,c):
    for roc in arg.rocs.split(','):
        for half in arg.half.split(','):
            values = delay_values
            for key in delay_values.keys():
                values = decay_values
                for val in range(0,8):
                    values[key] = val
                    print(f'Setting default delay parameters for roc {roc} and {half} and {key}:{val}')
                    for delay,delay_val in values.items():
                        c.roc_param(f"GLOBAL_ANALOG_{half}",delay,delay_val,[roc])
                        
                    if arg.pedestal:
                        c.daq_pedestal(nevents=arg.nevents,output_name=f"{arg.odir}/{key}{val}_{arg.nevents}.raw")
                    if arg.charge:
                        for ch in range(0,37):
                            c.set_charge_injection([roc],off=False,half=half,ch=ch)
                            c.daq_charge(nevents=arg.nevents,output_name=f"{arg.odir}/{key}{val}_{arg.nevents}.raw")
    c.write_exit()
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(f'python runBoardScan.py ',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--run',       action='store_true', dest='run',                 help='Run')
    parser.add_argument('--dpm',       type=int,            dest='dpm',    default=1,   help='DPM')
    parser.add_argument('--rocs',      type=str,            dest='rocs',   default='0', help='ROCs (separated by commas)')
    parser.add_argument('--half',      type=str,            dest='half',   default='0', help='Halfs (separated by commas)')
    parser.add_argument('--hdmi',      type=str,            dest='hdmi',   default='0', help='HDMI connectors (separated by commas). Use -1 to run all connectors.')
    parser.add_argument('--nevents',   type=int,            dest='nevents',default=100, help='Number of events')
    subparsers = parser.add_subparsers(help='Choose which action to perform.')

    parser_delay = subparsers.add_parser('delay', help='Scan values of ADC delay bits, setting all other delay bits to 1')
    parser_delay.add_argument('--pedestal',action='store_true',dest='pedestal',help='Take pedestal data after setting delay bits')
    parser_delay.add_argument('--charge',action='store_true',dest='charge',help='Set charge injection and take charge DAQ data after setting delay bits')
    parser_delay.set_defaults(action=delay_action)

    arg = parser.parse_args()

    if 'action' not in arg :
        parser.error('Must choose an action to perform!')
        
    import pfconfig
    with pfconfig.connect(f"cob1-dpm{arg.dpm}") as c:
        arg.action(arg,c)
        c.run(arg.run)
