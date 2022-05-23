import os
import glob
import numpy as np
import sys

def setup_pd_snapshot(input_snap,
                    output_dir='/nobackup17/gfsnyder/foggie-pd-outputs/',
                    pd_master_template='/home/gfsnyder/PythonCode/pdmocks/parameters_master.py',
                    pd_model_template='/home/gfsnyder/PythonCode/pdmocks/parameters_model.py'):

    #identify input snapshot
    print('setting up: ', input_snap)

    #create output directory
    snapname = os.path.basename(input_snap)
    runname = os.path.basename(os.path.dirname(input_snap))
    haloname = os.path.basename(os.path.dirname(os.path.dirname(input_snap)))

    print(snapname, runname, haloname)
    #copy parameter files to output directory


    #edit parameter files


    #create runscript




    return


if __name__=="__main__":
    input='/nobackup/mpeeples/halo_008508/nref11c_nref9f/DD1000'

    setup_pd_snapshot(input)
