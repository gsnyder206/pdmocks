import os
import glob
import numpy as np
import sys
import shutil
import astropy.io.ascii as ascii
import yt

foggie_repo_dir='/nobackupp17/gfsnyder/foggie'

def get_halo_center(snapname,runname,halo_number,ds):

    if runname=='natural':
        run_use='orig_nref11n'
    else:
        run_use=runname

    cv_file = os.path.join(foggie_repo_dir,'foggie','halo_infos',halo_number,run_use,'halo_c_v')
    print('cv_file: ', cv_file)
    if not os.path.lexists(cv_file):
        print('cv file not found, skipping!')
        return None,None,None

    cv_data=ascii.read(cv_file)
    print(cv_data[0:5])

    return x, y, z


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
    snapfile = os.path.join(input_snapdir,snapname)
    ds=yt.load(snapfile)

    output_dir=os.path.join(output_root,haloname,runname,snapname)
    os.makedirs(output_dir, exist_ok=True)

    #copy parameter files to output directory
    print('output dir: ', output_dir)
    shutil.copy2(pd_master_template,output_dir)


    #compute center from foggie halo_c_v files
    halo_number = haloname.split('_')[-1]

    x,y,z=get_halo_center(snapname,runname,halo_number,ds)

    #edit parameter files
    modelfile=os.path.join(output_dir,'parameters_'+snapname+'.py')
    mfo=open(modelfile,'w')

    mfo.write("hydro_dir = '"+input_snapdir+"/'\n")
    mfo.write("snapshot_name = '"+snapname+"'\n")

    mfo.write("PD_output_dir = '"+output_dir+"/'\n")
    mfo.write("Auto_TF_file = 'snap."+snapname+".logical'\n")
    mfo.write("Auto_dustdens_file = 'snap."+snapname+".dustdens'\n")

    mfo.write("inputfile = PD_output_dir+'/snap."+snapname+".rtin'\n")
    mfo.write("outputfile = PD_output_dir+'/snap."+snapname+".rtout'\n")

    #HAVE TO CODE THIS -- See Anna's code!
    mfo.write('x_cent = 0.5\n')
    mfo.write('y_cent = 0.5\n')
    mfo.write('z_cent = 0.5\n')

    mfo.write('TCMB = 2.73\n')

    mfo.close()


    #need to do any symlinking???

    #create runscript




    return


if __name__=="__main__":
    input='/nobackup/mpeeples/halo_008508/nref11c_nref9f/DD1000'

    setup_pd_snapshot(input)
