
## Computers : Data processing General nodes

# Data Policy 
!!! hint "Data policy"
      We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.



<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Beamline%20computers.png?raw=true)
</figure>


===============================================================================

!!! tip "Want to process the data after leaving beamline?"
    If you need more information [CHESS computing farm access](https://wiki.classe.cornell.edu/Computing/ComputeFarmIntro)

        Using general nodes follow the below steps
    

* Step 1 : login to `ssh <username>@lnx201.classe.cornell.edu`
* Step 2: `qrsh -q interactive.q -l mem_free=350G`
    
    Or if you need more core

* Step 2: `qrsh -q interactive.q -l mem_free=350G -pe sge_pe 20`
* Step 3: `source /nfs/chess/sw/anaconda3_jpcr/bin/activate`
* Step 4: `qstat`
* Step 5 : `ls`
* Step 6: `cd /nfs/chess/id4baux/2023-2/codebase_for_users/`
* Step 7: Follow `Step II` above 


<i> If you are doing stacking from general node, you need to change the permission setup </i>


### <b>Giving permission from your own account to chess_id4b to do rest of the processing follow the below steps </b>

* Step 1: If you are using general cluster, then follow the steps from your account 

    a) Go to the desired path
    b)  `chmod -R 777 (foldername)`


!!! tip "STEP II :  Stack data"

The script take all the detector's raw .cbf files and performed calibration. You can the get the [stack_em_all_cbf_2022.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/codebase_for_use/stack_em_all_cbf_2022.py). 

 
    Step 1 :  the `python stack_em_all_cbf_2022.py` python script
    Modify : 
            i) Project name : 
                            proj_name = "sarker-000-a/" (#project name)
            ii) Provide the .poni filename
                            calibfile = "/nfs/chess/id4baux/"+run_cycle+"+proj_name+"/calibration/ceria37keV.poni" 
            iii)Provide .edf filename
                            maskfile = "/nfs/chess/id4baux/"+run_cycle+"+proj_name+"/calibration/mask.edf" 
    
    Step 2 : Run python code
        Usage:
        python stack_em_all_cbf_2022.py    chem_formula sample_id spec_scan_num temperature

        Example: 
        >>>python stack_em_all_cbf_2022.py CoTiO3 sample 11 50

    Step 3 : Check data 
        After stacking is done the processed data will be avilable in id4baux folder    

You can create bash script to run the stacking 

        #!  /bin/bash
        python stack_em_all_cbf_2022.py CoTiO3 sample 11 50
        python stack_em_all_cbf_2022.py CoTiO3 sample 12 50
        python stack_em_all_cbf_2022.py CoTiO3 sample 13 50
    
===========================================================================

!!! tip "STEP III:  Find Bragg peaks"
[simple_peakfinder.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/simple_peakfinder.py) script

    Step 1: After stacking is done, take the whole stack from the id4aux data folder and run simple_peakfinder.py code
    
        Usage: 
        python simple_peakfinder.py /full/path/to/stack/ 0.95

        Example: 
        >>> python simple_peakfinder.py /nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/ 0.95

Would consider anything above 95% of max counts as a Bragg peak. You can change the thereshold  as needed. 
Check the number of peaks, you find after running the code. In between 200-3000 is a good number.  

===========================================================================

!!! tip "STEP IV:  Solve orientation matrix"
[auto_ormfinder.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/auto_ormfinder.py) script 

    Usage: 
    python auto_ormfinder.py */full/path/to/stack/ peakfilename.npy

    Example: 
    >>>python auto_ormfinder.py /nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/ peaklist1.npy

!!! danger "Please provide a space between pathname (/nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/) and peaklist1.npy"


===========================================================================

!!! tip "STEP V:  Convert stacks of data to HKL volume"

[Pil6M_HKLConv_3D_2022.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/Pil6M_HKLConv_3D_2022.py) python script (edit to point to project, ormatrix, and define HKL grid)

    Step 1: Edit the script
        i) Change the project name
                    projd = "/nfs/chess/id4baux/2022-3/sarker-0000-a"
                    sampldi = "/CoTiO3/sample/" 
        ii) Change the sample name:
                    sampldi = "/CoTiO3/sample/" 
        iii) Change the ormatix 
                    ormat = nxload(stackhklpath+"ormatrix_v1.nxs")
        iv) Define the hkl space to histogram
                    H= np.arrange (-5.1, 5.1, 0.01)
                    K= np.arrange (-5.1, 5.1, 0.01)
                    L= np.arrange (-5.1, 5.1, 0.01)
    
    Step 2: 
    Usage:
    python  Pil6M_HKLConv_3D_2022.py temperature

    Example:
    python Pil6M_HKLConv_3D_2022.py 50


!!! tip "Runnning same sample at different temperature processing"

* <i>Step A</i>: Do the stacking (follow `STEP I` above)
* <i>Step B</i>: Copy the `orientation matrix` from processed data
* <i>Step C</i>: Run `STEP V`



===========================================================================
!!! tip "login to jupyter"

To tunnel the jupyter notebook from a node to the browser on the station computer, try this:

* 1) setup your environment and start jupyter on the node (ie lnx306 or whatever) with
jupyter notebook --no-browser --port=8888 --ip="172.16.3.6"
* 2) from the station computer, open a new terminal and do
ssh -N -f -L localhost:8888:lnx306.classe.cornell.edu:8888
* 3) on the station computer, browse to localhost:8888 and enter the token as before (edited) 



### <b>Important links for more details </b>

* [Remote access to Linux machines](https://wiki.classe.cornell.edu/Computing/RemoteLinux)
* [Access to nomachine](https://wiki.classe.cornell.edu/Computing/NoMachine)
* [Data transfer Globus](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer)
* [CHESS computing farm access](https://wiki.classe.cornell.edu/Computing/ComputeFarmIntro)
* [CHESS jupyterhub](https://wiki.classe.cornell.edu/Computing/JupyterHub)
* [CLASSE-IT Service Requests ](service-classe@cornell.edu)


