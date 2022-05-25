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
    #print(cv_data[0:5])

    halo_i=cv_data['col3']==snapname
    xc=cv_data['col4'][halo_i]
    yc=cv_data['col5'][halo_i]
    zc=cv_data['col6'][halo_i]
    halo_center_kpc = ds.arr([float(xc), \
                            float(yc), \
                            float(zc)], 'kpc')
    halo_center_code = halo_center_kpc.in_units('code_length')

    return halo_center_code


def setup_pd_range(input_dir,begin_dd=100,end_dd=1500,skip=20,
                    output_root='/nobackupp17/gfsnyder/foggie-pd-outputs/'):

    ar=np.arange(begin_dd,end_dd,skip)#np.sory(np.asarray(glob.glob(os.path.join(input_dir,'DD????'))))
    dd=[]
    for ii in ar:
        dd.append('DD{:04}'.format(ii))

    runname = os.path.basename(input_dir)
    haloname = os.path.basename(os.path.dirname(input_dir))

    rundir=os.path.join(output_root,haloname,runname)
    os.makedirs(rundir, exist_ok=True)

    subscript=os.path.join(rundir,'submit_range.sh')

    ssfo=open(subscript,'w')


    dd = np.asarray(dd)


    for ddi in dd:
        #create individual stuff
        ddf = os.path.join(input_dir,ddi)
        qsub_fn=setup_pd_snapshot(ddf,output_root=output_root)

        #create bulk submission script
        ssfo.write('qsub '+qsub_fn+'\n')
    ssfo.close()

    return

def setup_pd_snapshot(input_snapdir,
                    output_root='/nobackupp17/gfsnyder/foggie-pd-outputs/',
                    pd_master_template='/home5/gfsnyder/PythonCode/pdmocks/parameters_master.py',
                    pd_model_template='/home5/gfsnyder/PythonCode/pdmocks/parameters_model.py',
                    ncpus=28,model='bro',walltime='24:00:00',queue='long'):

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
    print(x,y,z)
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

    mfo.write('x_cent = '+str(x.value)+'\n')
    mfo.write('y_cent = '+str(y.value)+'\n')
    mfo.write('z_cent = '+str(z.value)+'\n')

    mfo.write('TCMB = 2.73\n')

    mfo.close()


    #need to do any symlinking???

    #create runscript
    qsub_fn=os.path.join(output_dir,'pd.qsub')
    qfo=open(qsub_fn,'w')
    #qfo.write('#!/bin/bash\n')
    qfo.write('#PBS -S /bin/bash\n')   #apparently this is a thing
    qfo.write('#PBS -l select=1:ncpus='+str(ncpus)+':model='+model+'\n')   #selects cpu model and number (sunrise uses 1 node)
    qfo.write('#PBS -l walltime='+walltime+'\n')    #hh:mm:ss before job is killed
    qfo.write('#PBS -q '+queue+'\n')       #selects queue to submit to
    qfo.write('#PBS -N pd_run\n')     #selects job name
    qfo.write('#PBS -M gsnyder@stsci.edu\n')  #notifies job info to this email address
    qfo.write('#PBS -m abe\n')  #set notification types (abe=abort, begin, end)
    qfo.write('#PBS -o '+output_dir+'/pd_pbs.out\n')  #save standard output here
    qfo.write('#PBS -e '+output_dir+'/pd_pbs.err\n')  #save standard error here
    qfo.write('#PBS -V\n\n')    #export environment variables at start of job

    qfo.write('source ~/.bashrc\n')
    qfo.write('conda activate pdenv\n\n')
    qfo.write('module load comp-intel/2018.3.222\n')
    qfo.write('module load mpi-hpe/mpt.2.25\n')
    qfo.write('module load hdf5/1.8.18_serial\n\n')
    qfo.write('python /home5/gfsnyder/code/powderday/pd_front_end.py '+output_dir+' parameters_master '+os.path.basename(modelfile)[:-3]+'\n')


    qfo.close()

    return qsub_fn


if __name__=="__main__":
    #input='/nobackup/mpeeples/halo_008508/nref11c_nref9f/DD1000'

    #qfn=setup_pd_snapshot(input)

    input='/nobackup/mpeeples/halo_008508/nref11c_nref9f'
    setup_pd_range(input)
