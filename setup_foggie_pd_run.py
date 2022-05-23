import os
import glob
import numpy as np
import sys
import shutil

def setup_pd_snapshot(input_snapdir,
                    output_root='/nobackupp17/gfsnyder/foggie-pd-outputs/',
                    pd_master_template='/home5/gfsnyder/PythonCode/pdmocks/parameters_master.py',
                    pd_model_template='/home5/gfsnyder/PythonCode/pdmocks/parameters_model.py'):

    #identify input snapshot
    print('setting up: ', input_snapdir)

    #create output directory
    snapname = os.path.basename(input_snapdir)
    runname = os.path.basename(os.path.dirname(input_snapdir))
    haloname = os.path.basename(os.path.dirname(os.path.dirname(input_snapdir)))

    print(snapname, runname, haloname)


    output_dir=os.path.join(output_root,haloname,runname,snapname)
    os.makedirs(output_dir, exist_ok=True)

    #copy parameter files to output directory
    print('output dir: ', output_dir)
    shutil.copy2(pd_master_template,output_dir)

    #edit parameter files
    modelfile=os.path.join(output_dir,'parameters_'+snapname+'.py')
    mfo=open(modelfile,'w')

    mfo.write("hydro_dir = '"+input_snapdir+"'\n")
    mfo.write("snapshot_name = '"+snapname+"'\n")

    mfo.write("PD_output_dir = '"+output_dir+"'\n")
    mfo.write("Auto_TF_file = 'snap."+snapname+".logical'\n")
    mfo.write("Auto_dustdens_file = 'snap."+snapname+".dustdens'\n")

    mfo.write("inputfile = PD_output_dir+'/snap."+snapname+".rtin'\n")
    mfo.write("outputfile = PD_output_dir+'/snap."+snapname+".rtout'\n")

    mfo.write('x_cent = 0\n')
    mfo.write('y_cent = 0\n')
    mfo.write('z_cent = 0\n')

    mfo.write('TCMB = 2.73\n')

    mfo.close()


    #need to do any symlinking???

    #create runscript




    return


if __name__=="__main__":
    input='/nobackup/mpeeples/halo_008508/nref11c_nref9f/DD1000'

    setup_pd_snapshot(input)
