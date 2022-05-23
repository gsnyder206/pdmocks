import os
import glob
import numpy as np
import sys

def setup_pd_snapshot(input_file,
                    output_dir='/nobackup17/gfsnyder/foggie-pd-outputs/',
                    pd_master_template='/home/gfsnyder/PythonCode/pdmocks/parameters_master.py',
                    pd_model_template='/home/gfsnyder/PythonCode/pdmocks/parameters_model.py'):

    #identify input snapshot
    print('setting up: ', input_file)

    #create output directory


    #copy parameter files to output directory


    #edit parameter files


    #create runscript




    return


if __name__=="__main__":
    input=sys.argv[1]
    print(input)
