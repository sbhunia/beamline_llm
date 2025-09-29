# Welcome to Data Processing 

!!! type "NOTE"
    Single crystal data-processing codes are written by  [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) based on reference

    * [1] [H. You, J. Appl. Cryst.(1999).32, 614-623](https://onlinelibrary.wiley.com/doi/epdf/10.1107/S0021889899001223) and 
    * [2] [W. R. & Levy, H. A. (1967). Acta Cryst. 22, 457–464](https://scripts.iucr.org/cgi-bin/paper?s0365110x67000970)

The purpose of this guide is to illustrate some of the main features that Jacob's code provides. It assumes a very basic working knowledge with python pakages. To download the package please go to the github link. 

The code provides various tools for stacking the raw data, finding Bragg peaks, solving orientation matrix and finally provide the HKL. The results are visible to [NeXpy GUI](https://nexpy.github.io/nexpy/). 

# Data Policy 
!!! hint "Data policy"
      We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.

## Software

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/software.png?raw=true)
</figure>

---
### Single crystal data-processing steps
---

* `STEP I`:  Calibrate Detector & Beamline
* `STEP II`:  Stack data
* `STEP III`:  Find Bragg peaks
* `STEP IV`:  Solve orientation matrix
* `STEP V`:  Convert stacks of data to HKL volume 


!!! danger "Usage"

# Examples


!!! tip " Step I :  Calibrate Detector & Beamline" 


After collecting data from CeO2, LaB6, we calibrate the date by using pyFAI-calib2. Referemce shown below

Reference: 
pyFAI reference :[pyFAI](https://pyfai.readthedocs.io/en/master/).
pyFAI-calib2 : [calibration_video](https://pyfai.readthedocs.io/en/master/usage/cookbook/calib-gui/index.html#cookbook-calibration-gui) Calibration of a diffraction setup using the Graphical User Interface (GUI) 

    
    # Create calibration folder to the desired file location where new_averaged_file (i.e. ceria37keV.cbf) will save 
    >>> cd calibration

    #pyFAI-average -o <new_averaged_filename> <location of the datapath> <all the filenames> 
    #Example:
    >>> pyFAI-average -o ceria37keV.cbf /nfs/chess/id4b/2022-3/sarker-0000-0/raw6M/ceria/standard/300/ceria_001/ceria_PIL10_001_*.cbf``            #   generates average of all the images
    >>> pyFAI-calib2            #   generates .poni and mask.edf files

 After doing the calibration, save the .poni and mask file


===========================================================================

## Computers : Data processing 


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Beamline%20computers.png?raw=true)
</figure>


!!! danger "Recommendation : lnx306 to run the stacking code, HKL convertion code in lnx1034-f1"
In the beamline, you will find the folder `codebase_for_users` where all codes are saved. 
`lnx306` or `lnx1034-f1` can make ~3 stacks at a time before running out of the memory
`auto_ormfinder` and `Pil6M_HKLConv` both take all the CPUs. 



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


## Software NxRefine

For document, please visit the the [website documentation](https://nexpy.github.io/nxrefine/) written by Dr. Ray Osborn 

* <i>Setting up experiment







### <b>Important links for more details </b>

* [Remote access to Linux machines](https://wiki.classe.cornell.edu/Computing/RemoteLinux)
* [Access to nomachine](https://wiki.classe.cornell.edu/Computing/NoMachine)
* [Data transfer Globus](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer)
* [CHESS computing farm access](https://wiki.classe.cornell.edu/Computing/ComputeFarmIntro)
* [CHESS jupyterhub](https://wiki.classe.cornell.edu/Computing/JupyterHub)
* [CLASSE-IT Service Requests ](service-classe@cornell.edu)


