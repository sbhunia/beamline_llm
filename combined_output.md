

# Cryostat.md


#### Cryostat Installation 

* Step 1: Relocate the cryostream position
* Step 2: Stop the the 'phi' motor connection from MDCP, disengage it from the difractometer, unscrew the phi motor 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/phi%20motor%20removal.jpeg?raw=true){ width="250" }
</figure>


* Step 3 : Remove the goniometer sample stage 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/remove%20sample%20stage%201.png?raw=true){ width="600" }
</figure>

* Step 4 : Turn off the compressor by pressing 'off' button

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true){ width="300" }
</figure>

* Step 5: Wait until everything is 300K before turing off the cryostream 


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/lakeshore_temp_300_1.png?raw=true){ width="200" }
</figure>

* Step 6 : Disconnect the waterline and connect it to the lakeshore1

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/water%20connection.jpeg?raw=true){ width="200" }
</figure>


* Step 7:  Move the 6M pilatus detector at the end and place the 100K pilatus two theta to 0 degree. 
* Step 8: Move the difractometer 'chi' position 90 to 270. Place the sumitomoto stage from the top. Tighten that by key showed in the figure.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Stage_insert.png?raw=true){ width="500" }
</figure>


* Step 9: Place the sumitomoto sample stage from the top shown in (a) and (b). Tighten the screw shown in Figure (c)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sample_stage_1.png?raw=true){ width="500" }
</figure>

* Step 10: Rotate the whole stage 'phi' and 'chi' to take it dowm from chi 270 to 90. Make sure don't knock anything. 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/chi%20down.png?raw=true){ width="300" }
</figure>


* Step 11: Place to 0-ring to the sample stage.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Stage_O_ring.png?raw=true){ width="300" }
</figure>


* Step 12: Place the second part of the sample.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Stage_O_ring1.png?raw=true){ width="300" }
</figure>


* Step 13: Place the top part of the sample stage.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/top%20part.png?raw=true){ width="300" }
</figure>



* Step 14: Make sure the all the motor limits : theta, two theta, phi, chi 











---



# FAQ.md

## Frequently asked questions (FAQ)
!!! hint "Frequently asked questions (FAQ)"
    Answers are given by [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) and Suchismita Sarker



###### Q. How is the measurement time and what is the angle step size when rotating the single crystal?

These parameters are adjustable, of course, but the most “typical” choice is continuous rotation, 0.1 degree angular integrations, collecting 2 or 3 redundant 360 degree rotations with different rotation axes, and ~0.1 seconds per frame.  So, full data collection is ~3600 frames x 3 scans x 0.1 seconds = 18 minutes of data collection at a single temperature.  There is motor movement overhead that adds time to to this, but basically collecting one comprehensive dataset at one temperature in <30 minutes is reasonable>. 


###### Q. What is the photon energy and Qmax for 3D-PDF experiment?

Presently QM2 has a maximum operating energy of 52 keV. The minimum sample-to-detector distance with the Pilatus6M is ~380mm. This would give you a two-theta max < 45 degrees, and a QMax <~ 20 inv A, depending on how you center the detector on the beam.

###### Q. What is the temperature range available for 3D-dPDF? We are requesting cryostream-like temperature region (100~500 K), but it would be intesting to know if any lower or higher tempearture setup accessible.

Our gas cryocooler system gives the best quality data, since there are no windows. Our system operates using either helium or nitrogen, and can switch on the fly. With helium, it operates from ~13K to 180K, and with nitrogen from ~95K to 500K. When using this system, we recommend users mount samples using crystallography loops, as noted above.


##### Q. 2. What is the suitable single crystal size in volume and dimension lengths so that it can be covered by the beam when rotating (not too large or too small)?

 The beam at 4B is ~200 microns tall and ~1mm wide.  Typically, we mount crystals using mitigen crystallography loops if using a gas cryocooler, or on copper posts if using a closed cycle cryostat.  The ideal crystal size/shape depends a little on the mounting method. Generally, though, you want to keep the scattering volume constant while rotating, and you want to have crystals <~ one attenuation length in at least 2 dimensions. Samples can in principle be longer along the rotation axis direction - like a cylinder or bar where the short directions are ~ 100 microns but the long direction is several mm, still works well. 

###### Q: Where is my data?
The data stored at id4b, after processing the data your can find that in id4baux. 

###### Q: How to transfer the data?
You should use globus to transfer your data.


##### Q. How to recover if the computer fail?
Talk to the beamline scientist 


##### Q. Can I run thin-film samples at the beamline? What is the minimum thickness of the sample that can be examind?
Yes, thin-film samples can be successfully run at the beamline. The thinnest sample examined so far has had a thickness of 3 nm. 









---



# IC1_signal.md



### IC1 varies signal continuously fluctuating - maximum counts 

![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Iron%20chamber%20Issue.png?raw=true){ width="500" }


##### Inform beamline scientist 

* Step 1: Check the manual shutter : is it open? If not, go and click "Open" button 
* Step 2: Check the current (CESR) : Is it okay? If not, then follow the step 3
* Step 3: Go to mostab terminal and peak a number

![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sketchy_mostab.jpeg?raw=true){ width="500" }

* Step 4: peak a number 3 to "Turn feedback off"
* Step 5: wait until it maximize signal at IC1
* Step 6: peak a number 1 to Autotune 
* Step 7: wait until it maximize IC1









---



# ID4B_Codes.md

# Welcome to Data Processing 

!!! type "NOTE"
    Single crystal data-processing codes are written by  [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) based on reference

    * [1] [H. You, J. Appl. Cryst.(1999).32, 614-623](https://onlinelibrary.wiley.com/doi/epdf/10.1107/S0021889899001223) and 
    * [2] [W. R. & Levy, H. A. (1967). Acta Cryst. 22, 457–464](https://scripts.iucr.org/cgi-bin/paper?s0365110x67000970)

## Purpose and Scope
The purpose of this guide is to illustrate some of the main features that Jacob's code provides. It assumes a very basic working knowledge with python pakages. To download the package please go to the github link. 

Capabilities provided by the code: The code provides various tools for stacking the raw data, finding Bragg peaks, solving orientation matrix and finally provide the HKL. The results are visible to [NeXpy GUI](https://nexpy.github.io/nexpy/). 

#### Data Policy 
!!! hint "Data policy"
 Raw data are stored for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.

#### Software Overview

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/software.png?raw=true)
</figure>

#### Single crystal data-processing steps


* `STEP I`:  Calibrate Detector & Beamline
* `STEP II`:  Stack data
* `STEP III`:  Find Bragg peaks
* `STEP IV`:  Solve orientation matrix
* `STEP V`:  Convert stacks of data to HKL volume 

!!! danger "Usage"

## STEP I - Calibrate Detector & Beamline
!!! tip " Step I :  Calibrate Detector & Beamline" 

After collecting data from CeO2, LaB6, we calibrate the date by using pyFAI-calib2.

References: 
1. pyFAI reference :[pyFAI](https://pyfai.readthedocs.io/en/master/).
2. pyFAI-calib2 : [calibration_video](https://pyfai.readthedocs.io/en/master/usage/cookbook/calib-gui/index.html#cookbook-calibration-gui) Calibration of a diffraction setup using the Graphical User Interface (GUI) 

#### Commands and Procedure
    # Create calibration folder to the desired file location where new_averaged_file (i.e. ceria37keV.cbf) will save 
    >>> cd calibration

    #pyFAI-average -o <new_averaged_filename> <location of the datapath> <all the filenames> 
    #Example:
    >>> pyFAI-average -o ceria37keV.cbf /nfs/chess/id4b/2022-3/sarker-0000-0/raw6M/ceria/standard/300/ceria_001/ceria_PIL10_001_*.cbf``            #   generates average of all the images
    >>> pyFAI-calib2            #   generates .poni and mask.edf files

 After doing the calibration, save the .poni and mask file


#### Computers for Data processing 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Beamline%20computers.png?raw=true)
</figure>


!!! danger "Recommendation : lnx306 to run the stacking code, HKL convertion code in lnx1034-f1"
1. In the beamline, you will find the folder `codebase_for_users` where all codes are saved. 
`lnx306` or `lnx1034-f1` can make ~3 stacks at a time before running out of the memory
2. `auto_ormfinder` and `Pil6M_HKLConv` both take all the CPUs. 


## STEP II - Stack Data
!!! tip "STEP II :  Stack data"

This step takes all the detector's raw .cbf files and performed calibration.
Script: [stack_em_all_cbf_2022.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/codebase_for_use/stack_em_all_cbf_2022.py). 

## Configuration 
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
        
    Output: After stacking is done the processed data will be avilable in id4baux folder    

# Bash Script
You can create bash script to run the stacking 

        #!  /bin/bash
        python stack_em_all_cbf_2022.py CoTiO3 sample 11 50
        python stack_em_all_cbf_2022.py CoTiO3 sample 12 50
        python stack_em_all_cbf_2022.py CoTiO3 sample 13 50
    
    
## STEP III - Find Bragg Peaks
!!! tip "STEP III:  Find Bragg peaks"
[simple_peakfinder.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/simple_peakfinder.py) script

    Step 1: After stacking is done, take the whole stack from the id4aux data folder and run simple_peakfinder.py code
    
    Usage: 
    python simple_peakfinder.py /full/path/to/stack/ 0.95

    Example: 
        >>> python simple_peakfinder.py /nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/ 0.95

Any value above 95% of max counts as a Bragg peak. You can change the thereshold  as needed. 
Check the number of peaks, you find after running the code. In between 200-3000 is a good number.  


## STEP IV - Solve Orientation Matrix
!!! tip "STEP IV:  Solve orientation matrix"
[auto_ormfinder.py](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/auto_ormfinder.py) script 

    Usage: 
    python auto_ormfinder.py */full/path/to/stack/ peakfilename.npy

    Example: 
    >>>python auto_ormfinder.py /nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/ peaklist1.npy

!!! danger "Please provide a space between pathname (/nfs/chess/id4baux/2022-3/sarker-0000-a/CoTiO3/sample/300/) and peaklist1.npy"


## STEP V - Convert stacks of data to HKL volume
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


## PROCESSING THE SAME SAMPLE AT DIFFERENT TEMPERATURES
!!! tip "Runnning same sample at different temperature processing"

* Step A: Do the stacking (follow `STEP I` above)
* Step B: Copy the `orientation matrix` from processed data
* Step C: Run `STEP V`


## Software NxRefine

For document, please visit the the [website documentation](https://nexpy.github.io/nxrefine/) written by Dr. Ray Osborn 


### <b>Important links for more details </b>

* [Remote access to Linux machines](https://wiki.classe.cornell.edu/Computing/RemoteLinux)
* [Access to nomachine](https://wiki.classe.cornell.edu/Computing/NoMachine)
* [Data transfer Globus](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer)
* [CHESS computing farm access](https://wiki.classe.cornell.edu/Computing/ComputeFarmIntro)
* [CHESS jupyterhub](https://wiki.classe.cornell.edu/Computing/JupyterHub)
* [CLASSE-IT Service Requests ](service-classe@cornell.edu)




---



# ID4B_Codes_general_nodes.md


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


 If you are doing stacking from general node, you need to change the permission setup 


### Giving permission from your own account to chess_id4b to do rest of the processing follow the below steps 

* Step I: If you are using general cluster, then follow the steps from your account 

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




---



# PTZ_camera.md

## Cameras (ID4B Beamline)

Two Pan-Tilt-Zoom (PTZ) cameras are installed in the ID4B beamline.  
They are used by users to view the **sample position** and **computers**.

---

## PTZ Camera Locations and IP Addresses

### Hutch PTZ Camera
- **Purpose:** View the sample position inside the hutch
- **IP Address:** `192.168.182.82`

<figure markdown>
  ![Hutch PTZ Camera](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Hutch%20camera.jpeg?raw=true){ width="300" }
</figure>

---

### Station PTZ Camera
- **Purpose:** View the station area and computers
- **IP Address:** `192.168.182.42`

<figure markdown>
  ![Station PTZ Camera](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Sample%20camera.jpeg?raw=true){ width="300" }
</figure>

## Opening the Station Camera with Cursor  
*(If the station camera crashes)*

!!! danger "Opening the station camera with cursor (if it is crashed)"

### Step 1: Open the Terminal
Open a terminal window.

### Step 2: Launch ImageJ
Run: ImageJ










---



# SPEC_commands.md

# SPEC- ID4B
## Welcome to ID4B SPEC command

!!! hint "SPEC Detailed Descriptions"
For full documentation visit https://certif.com/.
In ID4B, we used several SPEC along with python and C written by Dr. Jacob Ruff.

## SPEC:
spec is internationally recognized as the leading software for instrument control and data acquisition in X-ray diffraction experiments.

---
!!! danger "SPEC Commands for ID4B"
More detaiils can be found in https://certif.com/ and ID4B-SPEC Examples.

## Important SPEC commands

- `mkdir` – Create a new directotry
- `a2scan` – Two-motor scan
- `abscan` – Incident-reflected angle scan
- `br` – br and ubr – move to the reciprocal space coordinates (HKL)
- `ca` – Calculate motor settings for a given point in reciprocal space
- `cal` – Calculate motor settings for a given point in reciprocal space
- `cat` – UNIX shell cat command
- `cd` – Change working directory
- `cmAX` – Compumotor AX motor controller
- `config` – Edit the hardware configuration
- `config_adm` – Configuration – administer hardware configuration file
- `constant` – Define a constant global symbol
- `counting` – Timer/scaler commands, macros and variables
- `cscan` – Continuous scans
- `ct` – Count and print results
- `dscan/lup` – Motor scan relative to the starting position
- `d2scan` – Two-motor scan relative to the starting positions
- `def` – Def and rdef – define a macro
- `disable` – Disable and enable – disable and enable hardware
- `do` – Execute a command file
- `dtscan` – Relative temperature scan
- `dxp` – XIA DXP CAMAC MCA
- `encode` – Encode()/decode() – data stream manipulation
- `epics` – EPICS specific functions
- `files` – Conventions for file/device output
- `flow` – Flow control
- `flyscan` – Continuous scans with multichannel scalers
- `fourc` – 4-circle geometry modes
- `funcs` – Functions – built-in functions
- `global` – Declare global variables
- `getE` – Get the energy
- `getroi` – Get the region of interest
- `hbeamscan` – Horizontal direction beam scan based on start, finish, interval and time arguments
- `history` – Command recall facility
- `hklscan` – General linear scan in reciprocal space
- `hscan` – Scan along the H-axis in reciprocal space
- `install` – SPEC installation procedure
- `l` – UNIX file listing
- `libedit` – Libedit/readline – command line recall and editing
- `lm` – List motor software limits
- `ls` – UNIX file listing
- `lscan` – Scan along the L-axis in reciprocal space
- `lup chi` – Motor chi scan relative to the starting position
- `lup th` – Motor theta scan relative to the starting position
- `lup tth` – Motor two-theta scan relative to the starting position
- `lup phi` – Motor phi scan relative to the starting position
- `macros` – Description of macro facility
- `matchUE` – Match undulator energy
- `maxk` – Maximum position at K reciprocal space
- `wm monchi` – Where is monochromator chi
- `mk / umk` – Move to the reciprocal space coordinates (HKL)
- `mono` – Monochromator control macros
- `motors` – Commands and functions for controlling motors
- `move_info` – move_info() – returns what would happen on a move
- `moveE` – Move the energy
- `mr` – Move to a given angle of specular reflection
- `mv` – mv and umv – move one motor
- `mvd` – Move a motor in dial units
- `mvr` – mvr and umvr – move a single motor relative to its current position
- `umv th CEN` – Move theta motor to center
- `mond` – Monochromator d position
- `montrav` – Monochromator in transverse direction
- `newvbeam` – New beam position based on vertical or horizontal beam scan
- `newfile` – Data file management
- `newmac` – Re-read the standard macro definitions
- `nu` – ???????
- `or0` –
- `or1` –
- `or_swap` –
- `os1` – Optical slit 1 position to 0
- `os2` – Optical slit 1 position to 0
- `pwd` – Print SPEC current working directory
- `pa` –
- `park6m` – Park the 6M PILATUS detector to 175m (x), 924.5m (y), 200m (z)
- `pil_von` – PILATUS video on
- `pil_voff` – PILATUS video off
- `pil_setdir` – PILATUS set directory
- `pil_setup PIL6` – PILATUS setup
- `pil_settrig "Internal"` –
- `pil_unsetup 0` – PILATUS unset
- `pl_xMAX` – Show maximum value of plot in x-direction
- `plotselect pilroi` – Plot select PILATUS ROI
- `qdo` – Execute a command file without echo
- `quickfly` –
- `quick_collect` –
- `rscan` – Specular reflectivity scan
- `r2scan` – Reflectivity background scans
- `readline` – Libedit/readline – command line recall and editing
- `resume` – Continue an aborted scan
- `roi` – Region of interest counters
- `samz` – Move sample z direction
- `scans` – Read data from ASCII SPEC scan files
- `server` – SPEC server/client remote control
- `set` – Define the user angle of a motor
- `setfilter` – Set filter
- `set_dial` – Define the dial position of a motor
- `setlat` – Set lattice
- `set_lm` – Set lower and upper software limits
- `set_sim` – Set simulate (no hardware) mode
- `setplot` – Set plotting options
- `setpowder` – Configure powder-averaged scans
- `setscans` – Configure scan options
- `showtemp` – Display current temperature
- `sharpopt` –
- `sixc` – 6-circle geometry modes
- `spec` – X-ray diffractometer operation for specific configurations
- `spec_menu` – Create interactive menu from specifications
- `spec_par` – Set internal parameters
- `splot` – Plot selected values
- `syncE` – Synchronize energy
- `tw tabzd tabzui tabzuo` – Tweak table
- `te` – Read or set temperature
- `teramp` – Ramp temperature to a new set point
- `tscan` – Temperature scan
- `th2th` – Theta two-theta scan
- `tw` – Tweak motors
- `tweakup` – Scan monochromator d, undulator optimization
- `unkludgenu` – ??????
- `vi` – Invoke standard UNIX visual editor
- `vscan` – Variable step size scans
- `vbeamscan` – Vertical beam scan
- `w` – Wait for moving and counting then beep
- `wa` – List all motor positions
- `wait` – Synchronization with moving and counting
- `wfilter` – Where are filters
- `wideopt` –
- `diftabx` – Diffractometer table x movement
- `diftabz` – Diffractometer table z movement
- `wh` – Where, principal axes and reciprocal space
- `whats` – Identify what an object is
- `wm` – Print motor positions
- `wmono` – Where is monochromatic beam
- `wmonoall` – Where motor positions including phi and filters
- `wmonoall` – Where is mirror position
- `wot` – Where is optical table
- `ws1` – Where is slit 1
- `ws2` – Where is slit 2
- `w6m` – Where is 6M detector
- `wslits` – Where are slit 1 and slit 2

If you encounter any new commands during your sample run, please email:
ss3428@cornell.edu


---



# SPEC_macros.md

# Welcome to SPEC macros
"NOTE": The code is written by [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) based on SPEC [certif.com](https://certif.com/).
"spec is internationally recognized as the leading software for instrument control and data acquisition in X-ray diffraction experiments."

# In ID4B, SPEC code is used along with python and C commands. ID4B beamline specific macros are shown below.

## Important SPEC commands for ID4B

* [`userlist.mac`](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/userlist.mac) - Important macos needed for the users, delaied descrispotion are shown below.

* JRs_useful_macros.mac – this is the mac file for beam, motor and slit positions  
* plotlast.mac – this is the mac file for generate??  
* undulator_macro.mac – this is the mac file for undulator stability  
* syncmon.mac – this is the mac file for syncronoze the system  
* fmbo_filter.mac – this is the mac file for filter macros  
* digio.mac – this is the mac file for diti?  
* set_and_get_rois.mac – this is the mac file for set ROI channels  
* multi_pilatus_v5.mac – this is the mac file for detector  
* Lakeshore336cryocool.mac – this is the mac file for temperature macros  
* energy_pv.mac – this is the mac file for energy macros  
* undulator_2A.mac – this is the mac file for undulator stablibility macros
    
## Detailed description of macros

The codes are in github repository [JRs_useful_macros.mac](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/JRs_useful_macros.mac)

1.  Define a macro vbeamscan based on passing four arrguments start, finish, interval and time parameter scans
2.  Define a macro newbeam based on passing four arrguments start, finish, interval and time parameter scans
3.  Define a macro hbeamscan based on passing four arrguments start, finish, interval and time parameter scans
4.  Define a macro monocromator position by "def wmono 'wm monu mond monoff montrav mond_x monzu monzd monxu monxd' "
5.  Define a macro for mirror posiiton by " def wmirror 'wm mird miru mirbd mirbu' "
6.  Define a macro for optical table
7.  Define a macro for slit position
8.  Define a macro for tweakup the monochromator d position wby scanning both mond and undulator motors
9.  Define where is 6M detectors
10. Define how to park the 6M detector






---



# about.md



Authors : User Guide of &#60QM&#62<sup>2</sup> beamline
<br>
<i> Staff scientist at CHESS ID4B <i>


Date: 
<br>
04-28-2025


---



# beam_dump.md



### After beam come back from long beam dump

* Step 1: Check the current (CERS)
* Step 2: After IC1 stabilized 
* Step 3: Open the shutter 'opens' 
* Step 4: Check the IC1

![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sketchy_mostab.jpeg?raw=true){ width="500" }

* Step 5: If you have singnal, some values at IC1
* Step 6: press 3 in stkechy_mostab
* Step 7: Use mostab go maximum IC2
* Step 8: Go to maximum IC1 
* Step 9: press 1 in stkechy_mostab



### If we are not using the mostab, follow the steps:


* Step 1: check the current
* Step 2: After it stabilized 
* Step 3: Check the shutter 
* Step 4: Check the IC1
* Step 5: If you have little counts at IC1 follow the below steps (if not talk to the beamline scientist):

* Manual: 
    * Turn the knob 

* In the SPEC terminal 

    * FOURC> `pil_off`
    * FOURC> `newfile align`
    * FOURC> `tweakup`
    * FOURC> `pil_on`

---



# beamline_basics.md



#### Where to check the CESR, Ion chamber 1 (IC1) , ion chamber 2 (IC2) and diode values?

* Make sure where you need you understand when the beam is in the hutch 
* You will have different vales (please check your google doc)
* If you see your diode values (showed in your google doc) are very different, contact beamline scientist
* Please igone other valuesin the panel

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/signals1.png?raw=true){ width="600" }
</figure>

#### What is SPEC?

SPEC is a UNIX-based software package for instrument control and data acquisition widely used for X-ray diffraction at synchrotrons around the world [1]

[1] [ More SPEC info](https://certif.com/spec.html)

#### Where are the different screen in the beamline computer?

!!! danger "DO NOT CLOSE ANYTHING"
      DONOT CLOSE ANYTHING (you will find out name of the program above the terminal)


!!! hint "<b> Screen 1 contains: </b> "
* SPEC terminal
* mostab terminal
* Ion chamber : SR570.adl,  SR570.adl,  SR570.adl
* Camera: ID4B: image1
* Camera controls: ID4B Sample View Controls
* ImageJ control


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Screen1.png?raw=true){ width="600" }
</figure>


!!! hint "<b> Screen 2 contains: (you don't need to use)</b> " 
* Detector EPICS controller

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Screen2.png?raw=true){ width="600" }
</figure>

<!-- !!! hint "<b> Screen 3 contains: (you can check few temperature parameters)</b> " 
* Temperature EPCS controller -->

### Screen 3 (you can check a few temperature parameters)

* Temperature EPICS controller

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Screen3.png?raw=true){ width="600" }
</figure>

!!! hint "<b> Screen 4 contains: (you don't need to use)</b> " 
* ImageJ EPICS controller

!!! hint "<b> Screen 5 contains: (you need to use)</b> " 
* Google doc and 
* Web camera

!!! hint "<b> Screen 6 contains: (you need to use)</b> " 

* Raw data visulization software

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Screen6.png?raw=true){ width="600" }
</figure>


---



# beamline_parameters.md


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/users_to_pub.png?raw=true)
</figure>

## Plan to apply the beamline?

The following links are required to apply for beamline:

* #### Deadline for the proposal : [CHESS Proposal Submission Deadline](https://www.chess.cornell.edu/users/chess-deadlines)

* #### Experimental hutch : [Want to see the hutch?](https://my.matterport.com/show/?m=Sfd6R3am1wR)  Password: CHEXSQM2

* #### CHESS User Guide : [CHESS User Guide](https://www.chess.cornell.edu/user-guide)


* #### CHESS User Agreement : [CHESS User Agreement](https://www.chess.cornell.edu/user-agreement#:~:text=In%20exchange%20for%20use%20of,of%20the%20negligence%20of%20Cornell)




# Data Policy 
!!! hint "Data policy"
      We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.


#### Link for the Data transfers 

* [Remote access to Linux machines](https://wiki.classe.cornell.edu/Computing/RemoteLinux)
* [Access to nomachine](https://wiki.classe.cornell.edu/Computing/NoMachine)
* [Data transfer Globus](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer)





#### Beamline Parameters


| Attibutes | Specifications | 
| -------------- | :---------: | 
| Available techniques | HDRM, REXS | 
| Source | CHESS compact Undulator | 
| Brilliance| 10^12 ph/s/0.1%bw/mm^2 | 
| Current| 100 mA | 
| Energy range | 6-70 KeV | 
| Energy resolution | dE/E ~ 10-4 | 
| Monochromator | DCM Diamond |
| Focusing mirror | Silicon with Rh coated |
| Detection mode | Transmission |  
| Detector| Pilatus 6M | 
| Spot size| 300 microns x 800 microns | 
| Time to take the data| HRDM ~ 20 mins | 





---



# beamline_setup.md


#### Beamline Startup 

#### Parameters of the beamline


| Attibutes | Specifications | 
| -------------- | :---------: | 
| Available techniques | HDRM, REXS | 
| Source | CHESS compact Undulator | 
| Brilliance| ?? ph/s/0.1%bw/mm^2 | 
| Current| 100 mA | 
| Energy range | 7-52 KeV | 
| Energy resolution | | 
| Maximum flux | | 
| Resolution power | | 
| Monochromator | DCM Diamond |
| Focusing mirror | Silicon with Rh coated |
| Detection mode | Transmission |  
| Detector| Pilatus 6M | 
| Spot size| 200 microns x 500 microns | 
| Time to take the data| HRDM ~ 20 mins | 


#### General steps

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/users_to_pub.png?raw=true)
</figure>


#### Instruction for nomachine

Please [click the link](https://wiki.classe.cornell.edu/Computing/NoMachine) for nomachine connection in your system.


#### Instruction for Globus

Please [click the link](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer) for data transfer. 

show_apms 1
show_apms 2
show_apms 3

# Group permission
https://wiki.classe.cornell.edu/Computing/CLASSEGroupManagement


---



# camera_image_stuck.md


# Camera image stuck

##### Inform beamline scientist 

* Step 1: Close all the imageJ
* Step 2: Open terminal
* Step 3: > `sample_view_camera_restart`
* Step 4:  > `ImageJ ID4B &` (for top camera)

# ImageJ not working 

##### Inform beamline scientist 

* Step 1: Make sure you closed every terminal of ImageJ
* Step 2: Open terminal
* Step 3: > `ImageJ ID4B &` (for top camera)
* Step 4: > `ImageJ ID4B_T` & (for bottom camera)

---



# comp_issues.md



Contact IT if you have any issues, send an email to please <a href = "mailto: service-classe@cornell.edu">send an email to CLASSE IT</a>.

* Problem to longin lnx201

    * 1st follow the steps :  [https://wiki.classe.cornell.edu/Computing/RemoteLinux](https://wiki.classe.cornell.edu/Computing/RemoteLinux)

* Problem with accessing data via Globus
    * 1st Floow the steps: [https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer](https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer)







---



# controlC_question.md



### Control C middle of the run questions

If you saw the below message for `samx` , `samy` , `samz` and `phi`, please say `y`

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/new_sample_motor.png?raw=true){ width="800" }
</figure>





---



# cryo_fail.md



#### Emergency proceduce if the temperature controller fails or Sudden power failure at beamline

!!! danger "Talk to Beamline Scientist or operators --- DONOT TRY THIS WITHOUT ASKING" 
If you suddenly saw the temperature controller is not showing the desired temperature

* If the your setup is in nitrogen condition (300K - 80K) and suddenly temperature is dropiing drastically and you don't have controls 
  * Switch the valve Nitrogen to Helium 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true){ width="500" }
</figure>

  * press `off` in the compressor (it is inside the hutch)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true){ width="300" }
</figure>

  * Change the EPIC PVs range manually
    * Go to screen 3 of the beamline computer
    * Find the CS-Studio for temperature
    * Click the `output 1` 
    * Go to range and select `Range3/High` for Input A
    * Click the `output 2`
    * Go to range and select `Range3/High` for Input B
    * Click the `output 3`
    * Go to range and select `On` for Input C
    * Click the `output 4`
    * Go to range and select `On` for Input D

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/cryostrem%20range.png?raw=true){ width="300" }
</figure>




---



# cryocooler.md

## Cryocoolers



<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/Crysocooler.png?raw=true)

</figure>

The cryocooler is manufactured by [CYRO Industries of America, Inc.](http://www.cryoindustries.com/).

<i> Close-circle cryostats are installed in &#60QM&#62<sup>2</sup> allowing samples to be comprehensively studied in a wide range of temperatures from 12K to 500K. The cryocooler can operate both helium (12K to 300K) and nitrogen gas (300K to 500K ) using a single stream flow. In-house nitrogen and helium gas are used for cryocoolers. Just by switching the knob outside of the hutch, the gas supply can be altered. 

The external tip-heater prevents frost and maintains a dry tip that helps to create an ice-free sample environment at low temperatures. A platinum temperature sensor is installed to control the low alarm setting temperature that triggers back the temperature controller to energize and maintain the ice-free environment. 

The five components of cryostat are: 


* 1. source  : the refrigerator or the cryostat act as a source to cool a reliable cryogenic temperature for a long continuous periods


* 2. compressor 


* 3. PID temperature controller : Cryogenic temperature controlled Model 336 manufactured by Lake Shore is used.  The controller’s zone tuning feature allows you to measure and control temperatures seamlessly from 300 mK to over 1,500 K by automatically switching temperature sensor inputs [1].


* 4. Power supply  : 30 V digital and 24V DC are used
 

* 5. Gas flow controller  : The digital flow automatically control and displays the flow rate

 - Gas flow parameters 

 - Helium gas: Normal flow rate is between 8 – 12 liters/min, typically 11 l/min

 - Nitrogen gas  : Normal flow rate is between 8 – 12 liters/min, typically 9 l/min.


 Safety 

* Do not touch the cold helium and nitrogen gas stream. Exposure to the skin of the cold gas could result in severe injuries.
* The dewar system has pressure relief protection installed. Do not remove pressure reliefs or check valves.

### Cryocooler temperature control / Motors

The cryocooler temperature is controlled via the following motor interface:
                                                              
* Motor : Temperature Controller
* Commands : sampleT
* Comments : Set the temperature


### To open the lakeshore

* Step 1:Open terminal
* Step 2: > `cd` 
* Step 3:  > `/mnt/home/chess_id4b/.cs-studio` 
* Step 4: click okay
* Step 5: In the file you can find the recent window for lakeshore.opi
* Step 6: click lakeshore 2
* Change the  Range : Rang3/High  



!!! danger "Practical guide of the temperature switch between nitrogen and helium"

[Temperature change guideline](https://suchismitasarker.github.io/CHESS-ID4B-QM2/temp/)


---



# detector_information.md


# Detectors
1. Pilatus 6M 
2. Pilatus6 100K 
3. Pilatus8 100K


## Technical Details
#####   Pilatus 6M 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/detector.png?raw=true)
</figure>

The large (W 590 x H 603 x D 455 mm<sup>3</sup>) Dectris Pilatus 6-megapixel photon counting detector shown above. 
<br>
The 6M high-dynamic-range hybrid pixel array detector was designed by Paul Scherrer Institute and sold by Dectris. The 6M Pilatus3 X series single photon counting detector has unprecedented count rate, direct detection of x-ray in single-photon-sensitivity, higher dynamic range (no dark current and no readout noise), higher frame rate, higher maximum count rate, millions of pixels and room temperature operations to reveal the weak features associated with Bragg peaks in diffuse scattering.

The Pilatus 6M detector have pixel  size  of  172x172 µm²,  2463x2527 pixel array, 423.6 x 434.6 mm² active area,  100 Hz frame rate,  20-bit/pixel  dynamic  range, count rate 10 <sup> ph/s/pixel </sup>  and  readout  time  of  0.95  ms [[1](https://www.dectris.com/)]. 



<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/6M%20image.png?raw=true)
</figure>
<b> Figure : Scattering data from Pilatus 6M </b> taken by Dr. Ruff at &#60QM&#62<sup>2</sup>

---

Table 1 : Detector Paramters

| Attibutes | Specifications | 
| -------------- | :---------: | 
| Dectector | 6M Pilatus3 | 
| pixel  size | 172x172 µm²| 
| pixel array | 2463x2527 | 
| active area | 423.6 x 434.6 mm² | 
| Frame rate | 100 Hz | 
| Dynamic  range | 20-bit/pixel | 
| count rate  | 10 <sup> ph/s/pixel </sup> | 
| readout  time  | 0.95  ms | 





Table 2 :  Pilatus commands

| Motor | Commands | Comments | 
| -------------- | :---------: | ---------- |  
| PILATUS 6 | PIL6 | Pilatus 6M detector | 
| PILATUS 6 | Pil6my | Move pilatus 6M detector in Y direction |
| PILATUS 6 | Pil6mz | Move pilatus 6M detector in Y direction |
| PILATUS 6 | Pilroi | Pilatus 6M detector region of interest |


#### Pilatus6 100K 

The link for the technical details are [here](https://media.dectris.com/Technical_Specification_PILATUS_100K-S_V1_8.pdf) 




#### Pilatus8 100K and Pilatus6 100K

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Piltatus%20100K.png?raw=true)
</figure>







---



# diffractometer.md


#### Huber diffractometer

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/Diffractometer-directions-v1.png?raw=true)
</figure>


<i> Huber “psi” diffractometer is installed at CHESS ID4B. Due to four sample-orientation axes and two detector-orientation axes, the psi-circle diffractometer is also known as “4S+2D". The independent motion sample and detector orientation provide nine degrees of freedom to define any vertical diffraction plane.The angle calculations for this diffractometer were shown in the reference [1] [2]. The motor names are shown below in Table 1. 

<b>Reference</b>
<br>
[1] H. You, J. Appl. Cryst.(1999).32, 614-623 and
<br>
[2] W. R. & Levy, H. A. (1967). Acta Cryst. 22, 457–464
</i>
</br>



<b> Table 1 </b> : Names of the six-circle Huber Diffractometer's motor

| Motor | Commands | Comments | 
| -------------- | :---------: | ---------- | 
| 2-Theta | tth | horizontal axis for detector arm |  
| Theta | th | horizontal axis for sample | 
| Chi | chi | sample motor | 
| Phi | phi | sample motor |  
| Nu | nu | vertical axis for detector, only for psic | 
| Mu | mu | vertical axis for sample, only for psic |
| X-direction | samplex | sample motor x-direction |  
| Y-direction | sampley | sample motor y-direction | 
| Z-direction | samplez | sample motor z-direction |


<b> Table 2 </b>  : Motor range and accuracy

| Motor | Range (deg) | Accuracy (arcsec) | Spheres of confusion  | Comments|
| -------------- | :---------: | ---------- | ---------- | ---------- |  
| Theta | -10/+90? | 0.18? |  30? | vertical theta
| Delta |  | 0.18? |  30? | vertical 2theta
| mu | -- | 0.18? |  30? | horizontal theta
| gamma | --  | 0.18? |  30? | horizontal two theta
| Chi| -- | 0.18? |  30? | with and without cryostat
| Phi| -- | 0.18? |  30? | 


---



# energy_change.md


### Start the new users at the beamline
* `newmac` (# <i> uploading all the macros </i>)
* `userslist.mac`
* `cd Scripts/`
* `./newusers-4b.sh 2022-3 sarker-0000-a` ( <i>this will create file both in id4b and id4baux </i>)
* copy HRDMscans.mac to the specific folder
* FOURC > `qdo ./HRDMscans.mac`
* FOURC > `newfile (name of newfile)`
* Change the HDRMscans.mac file with `_samplename` and `_sampledirectory`


### Open the camera inside the front hutch
* Open an terminal
*  type `vimba`
* Vimba viewer will open with two cameras ( IP addresses: 1st crystal:  `192.168.180.102`, 2nd crystal : `192.168.180.101`)

### Open ion chambers

* Open an terminal 
* type `show_apms 0`
* type `show_apms 1`
* type `show_apms 2`

### for FOURC opening

* Open an terminal 
* type `fourc`
* press `yes` if fourc ask questions to change motor values



#### Flux Calculator
[CHESS Flux calculator](https://www.chess.cornell.edu/userstechnical-resourcescalculators/ion-chamber-flux-calculator) at the beamline

#### X-ray absoption edge 

[Check absroption edge](http://skuld.bmsc.washington.edu/scatter/AS_periodic.html)


#### flyscan 
* `flyscan_setup`
* selecct motor using space 
* check flyscan
* FOURC > `powderscan 300 1`


### User HDRMScan details about the macros
#### Energy change
##### Removing mirror for higher energy calibrations

'''

        newfile 
        wmirror
        umvr  mird  miru    
        opens
        wot
        tw tabzd    tabzui    tabzuo  
        ws2
        wot
        wm diftabz
        tw tabzd    tabzui    tabzuo  
        tw tabxd
        closes
        syncE

'''


##### Energy calibrations


'''

            moveE 25
            umvr mond
            matchUE 8
            tweakup
            wm
            lup montrav -3 3 60 0.1
            umv montrav 163.98
            tweakup
            wm monchi
            Tw monchi
            lup monchi -0.5 0.5 20 0.1
            plotselect ic2 diode
            splot
            Plotselect ic2
            splot
            syncE
            plotselect ic2 diode
            splot
            umv monchi pl_xMAX
            getE

            wot
            ws1
            tw tabzd    tabzui    tabzuo 1 1 1
            tw tabxd .05
            tweakup
            syncE
            moveE 30.6; matchUE 8


'''

Step I: 
* Cover the detector
* Before energy change (> 30 keV higher to lower < 18 keV)
         verify counts in ic1, ic2 and diode (`getE` : provide you the energy)
         Put mostab to 5 V 
         Optimize counts (`tweakup`)
         `syncE`
* Then try move energy and optimize mostab:
        `moveE 11`
        `matchUE 3`
        `tweakup`
        `lup montrav`
* Open shuttur
        `os1 4 4`
* move the whole table up 
        `tw tabzu tabx tabzui 1 1 1 `

* Get values in ic1 and ic2 
* put mirror 
        `wmirror`



Cryo
* take out the stage
* Go to chi 90
* put the new sample stage with pin (the pin should slide in the sample stage) 
* Put the cryostate : it will go only from one side shown in the below
* there are 4 scrwes to hold that(8'32)
* Config X, Y, Z  (cryz, cryx, cryoy)
* wm cryx cryy
* check the phi and beamstop *
* check cryoz wihth signal
* up the resonance, so we should 
* tw crx .2, the crystal beam is there
* restrict the phi 
* tw cry cetered
* tw cryoy centered
* ca 002
* umv tth 20.2 th 0 chi 90
* See signal 
* freeze  phi -180
* ubr 2 -2 2 
* `cuts` (not contunuously moving )
* phi is fixed, others are moving with ubr 2 -2 2 
* FInd cryx cryy cryz (florescence)
* Tw th
* freeze phi -90
* ca 0 0 2
* calibration 
* ca 0 02 
* ubr  0 0 2 
* th2th -1 1 40 1
* opt2 (optimizing theta, phi and chi)
* pa (got statistics)
* ca 102 
* ubr 1 0 2
* wh 
* ubr 1 0 2
* pil_voff 
* pil_on
* check the fitter 
* th2th -2 2 60 1 
* manually optimize 
* optimize theta, phi and chi
* useful.mac "cryocool to simitomo "
* config file : lakeshow1: kG1 
* prdef measured temp
* open temperature terminal : css (lakeshore controller)
* File > lakeshoreopi > lakeshore1
* Lakeshore1.Kr00 (change range in the plot)
* we need to remove the filter to see the magnetic peaks



Tommorw : 
* Turn off the lakeshore 
* Wait for temperature to selle in 
* close the vaccum 
* SLowly break the vaccum (remove o-ring)
* Give some time to settle in 
* Remove 4 scews remove the sample 




### Detector setup

REXS 

Setup : 

mv pil6mx 100
mv pil6my 760

* `mv pil6mx 100` 		- move pilatus 6M to 100 mm x direction 
* `mv pil6my 760` 		- move pilatus 6M to 760 mm y direction


To take the detecotor all the way end of the hutch 

mv pil6mx 233
mv pil6my 885

* `mv pil6mx 233` 		- move pilatus 6M to 233 mm x direction 
* `mv pil6my 885` 		- move pilatus 6M to 885 mm y direction


### Change the config file 

open the terminal

```
config 
config configaration will open
Go to the specific motor 
change the required motor config
press w 
control c 
reconfig
```
To go to the specific motor press c,c (twice)   
shift+' to modify anything
     




---



# gas_flow.md


# Gas flow control


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/gas_flow_1.png?raw=true){ width="500" }
</figure>

It is important to control icing or heating by modifying nitrogen or helium gas flow. Follow the below steps to change the gas flow

Automated gas flowrate change: talk to the staff scientist 
        
  * `FOURC> flow_set <number>`
  * `FOURC> flow_get `


Manually change the flowrate 

* Step 1 : Press ENT in the gas flow meter
* Step 2 : Press up or down arraow to change the number (right now it is showing 9.04 liter/min in the above gas flow meter)
* Step 3 : Right or left arrow will take you to the desired digits
* Step 4 : Press ENT again in the gas flow meter, it will go show the desired final values
* Step 5 : If you don't need to change anything, press ESC







---



# index.md


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/CHESS-beamlineI.png?raw=true)
</figure>

# Welcome to CHESS Quantum Materials Beamline Documentation!

The Q-Mapping for Quantum Materials beamline is optimized to uncover intertwined quantum correlations of spins, charges and orbitals, over a wide temperature range and spanning entire phase diagrams. 

For comprehensive documentation of its capabilities, please visit (https://www.chess.cornell.edu/users/qm2-beamline). This document provides a collection of code snippets and equipment details that are essential for the operation of beamline ID4B at CHESS. If you encounter with any bug or like to have additional functionality, please send an email to ss3428@cornell.edu"> ID4B beamline.


### What does the beamline do?

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/QM2%20beamline%202025%20v1.png?raw=true){ width="700" }
</figure>

### Publications:  [List of beamline publications](https://suchismitasarker.github.io/CHESS-ID4B-QM2/publications/)


### contact Information for exploring new sample environments 
Please send an email to ss3428@cornell.edu ID4B beamline and check our [sample environment page](https://suchismitasarker.github.io/CHESS-ID4B-QM2/sample_env/)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Quantum%20control.png?raw=true){ width="700" }
</figure>

---

---

# User Documentations

* [Getting Started](https://suchismitasarker.github.io/CHESS-ID4B-QM2/beamline_parameters/) 
* [ID4B-SPEC commands](https://suchismitasarker.github.io/CHESS-ID4B-QM2/SPEC_commands/) 
* [Data processing](https://suchismitasarker.github.io/CHESS-ID4B-QM2/ID4B_Codes/)


# Sample alignment

* [Sample Alignments](https://suchismitasarker.github.io/CHESS-ID4B-QM2/sample_alignment/#) 
    * [High Dynamic Range Reciprocal Space Mapping (HDRM)](https://suchismitasarker.github.io/CHESS-ID4B-QM2/sample_alignment/#basic-steps-for-sample-alignment-hdrm)
    * [Resonant Elastic X-ray Scattering (REXS)](https://suchismitasarker.github.io/CHESS-ID4B-QM2/sample_alignment/#basic-steps-for-sample-alignments-rexs)



# Beamline details

  * [Beamline Layout](https://suchismitasarker.github.io/CHESS-ID4B-QM2/introduction/)
  * [Diffractometer](https://suchismitasarker.github.io/CHESS-ID4B-QM2/diffractometer/)
  * [Cryocooler](https://suchismitasarker.github.io/CHESS-ID4B-QM2/cryocooler/)
  * [Detector information](https://suchismitasarker.github.io/CHESS-ID4B-QM2/detector_information/)



# Frequently Asked Questions (FAQ)
* [Questions](https://suchismitasarker.github.io/CHESS-ID4B-QM2/FAQ/) 

---


---



# information.md


## Plan to apply the beamline?

* ####  Deadline for the proposal :  [CHESS Proposal Submission Deadline](https://www.chess.cornell.edu/users/chess-deadlines)

* ####  Experimental hutch :  [Want to see the hutch?](https://my.matterport.com/show/?m=Sfd6R3am1wR)  Password: CHEXSQM2

* ####  CHESS User Guide :  [CHESS User Guide](https://www.chess.cornell.edu/user-guide)


* ####  CHESS User Agreement :  [CHESS User Agreement](https://www.chess.cornell.edu/user-agreement#:~:text=In%20exchange%20for%20use%20of,of%20the%20negligence%20of%20Cornell)



## Before coming to the beamline, please email ss3428@cornell.edu and answer the following-


*  Question 1 . Have you run any experiments at QM2 earlier?
*  Question 2 : How many people are planning to come to beamline? Please send name and email information.
*  Question 3 : Safety training and other information: contact CHESS user office.
*  Question 4 . What kind of experiments are you planning to run at the beamline? HDRM,  REXS or HiTp XRD?
*  Question 5 : Is it air sensetive sample? Do you need a glove box?
*  Question 6 : Is there any special equipment you want to bring to the beamline?
*  Question 7 : Is it a thin-film or single crystal sample? Please provide the size of the samples
*  Question 9 : Mount your samples before coming to the beamline more details are at (https://suchismitasarker.github.io/CHESS-ID4B-QM2/sample/).
*  Question 10 : Do you have any energy preference for the samples?
*  Question 11 : Do you need to check the sample quality ? Or do you need to find a good crystal?
*  Question 12 : Do you want to perform crystallography?
*  Question 8 : Send the list of samples and desired sample temperatures before coming to the beamline.
        
        Example
            | Sample name | Temperature (K) | 
            | :----------:| :---------------: 
            | AV3Sb5      |       300       |  
            | AV3Sb5      |        75       | 
            | AV3Sb5      |        15       | 





========================================================================
## Computer resources:

*  Remote access to Linux machines  : https://wiki.classe.cornell.edu/Computing/RemoteLinux
*  Namachine access  : https://wiki.classe.cornell.edu/Computing/NoMachine
*  Data access  : https://wiki.classe.cornell.edu/Computing/GlobusDataTransfer
*  CLASSE-IT Service Requests  : service-classe@cornell.edu  


---



# introduction.md

# Introduction

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/beamline%20schematic.png?raw=true)
</figure>

The layout of the CHESS ID4B beamline is shown in the figure above. For more details see the beamline paper (soon to be published). 

This document is categorized into three sections. 

* [User Guide :(https://suchismitasarker.github.io/CHESS-ID4B-QM2/#) This is the most useful section for the ID4B beamline users. Here, the users can gather information about SPEC commands to run their samples in the beamline. This includes sample alignment details and data analysis steps. In addition, this section also includes information on the beamline equipment.


* [Admin documents(https://suchismitasarker.github.io/CHESS-ID4B-QM2/beamline_setup/) : This section is used for administrative purposes. However, you can find information about proposal details, and computational configurations (nomachine and globus setup) in the beamline setup section.


* [Frequently Ask Questions (FAQ) (https://suchismitasarker.github.io/CHESS-ID4B-QM2/FAQ/) :   This section includes FAQs in the beamline before, during, and after the run. 
  [`Please read the questions and answers, you might find yours!!`](https://suchismitasarker.github.io/CHESS-ID4B-QM2/FAQ/)    



### Do you want to see inside the hutch?

[CHESS ID4B hutch](https://my.matterport.com/show/?m=Sfd6R3am1wR)
Password: CHEXSQM2







---



# lost_fourc.md

#### STEP 1: If you lost fourc/SPEC terminal 
* Open terminal 
* type `findspec` (it will provide all the spec information)
* If SPEC is open it will go to the SPEC terminal
*  Skip the below steps 
    * Check the getPid number (you do not have to do this step)
    * type `fg <getPid number>` (example # fg 21192)  (you do not have to do this step)

##### STEP 2: SPEC is still missing

If you doesn't find anythng after STEP 1 fourc/SPEC terminal 

*  Talk to beamline scientist  
* If you not find the SPEC terminal, then type below command
* `kill -9 <getPid number>` (example# kill -9 21192)
* Open a new terminal 
* Type `fourc`

###### If you fourc/SPEC doesn't work 

* Open terminal 
* type `quit`
* type `fourc`

link for the new_sample_motor is:
https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/new_sample_motor.png


---



# lower_diode_signal.md


If you have a lower diode signal then: 
#### STEP 1: STOP the experiment
#### STEP 2: Talk to beamline scientist






---



# mostab-- no info here and on website.md



# If you have mostab issues








---



# nexpy.md


# Nexpy
The code provides various tools for stacking the raw data, finding Bragg peaks, solving orientation matrix, and finally providing the HKL. The results are visible to [NeXpy GUI](https://nexpy.github.io/nexpy/).


!!! danger "Recommendation to take a look at data visulization package" 
[Nexpy visulization Documentation](https://nexpy.github.io/nexpy/pythongui.html)

#### Quick video on 'heightscan' visualization:
"https://www.youtube.com/embed/lC853bBnRas?si=OLcOmv5HoKCyejph" 

 

### Steps to use the NexPy at beamline

####  Step 1 : Open the Nexpy (Beamline scientist only)

* Terminal > `ssh -Y lnx1034-f1`
* Terminal > nexpy &

####  Step 2  : Take a look at the priliminary data after data collection 

* a. Go to 'File' tab
* b. Go to 'Import' tab 
* c. Go to 'Import image stack'
* d. Go to desired file location
* e. Select the folder (it will not show any images)
* f. Select the images (mostly 50-60 images)
* g. Double clicked the stack images
* h. Go to the signal and click log scale
* i. Go to z tab and press forward (it will go through the images)


#### Quick video on 'collected data' visualization 
"https://www.youtube.com/embed/iyH_1zRsjmg?si=pW0kxtrW19vN1Gd3"






---



# nexpy_crushed.md

#### If nexpy is crushed on a beamline computer:

* Step 1: Make sure it is not open in another screen
* Step 2: In the screen 7, you will find the terminal name of nexpy 
* Step 3: Press enter 
* Step 4: Make sure you are at lnx306 computer `(base) [chess_id4b@lnx306 ~]$`
* Step 5: Type `nexpy &`

#### If nexpy is crushed on a Data analysis computer:

* Step 1: Make sure it is not open in another screen
* Step 2: In the screen 1, you will find the terminal name of nxrefine 
* Step 3: Press enter 
* Step 4: Make sure you are at lnx1034-f1 computer `(nxrefine) [chess_id4b@lnx1034-f1 ~]$` with the environment of `nxrefine` 
* Step 5: Type `nexpy &` 

---



# nxrefine.md


# NXRefine
The code is written by Dr. Ray Osborn. More details will be available [NXRefine](https://nexpy.github.io/nxrefine/).The code provides various tools for stacking the raw data, finding Bragg peaks, solving the orientation matrix, and finally providing the HKL. 

# Data Policy 
!!! hint "Data policy"
      We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.

### Steps to use the Nexrefine at CHESS beamline

####  Step 1 : Link raw data to process data folder

* A quick youtube video link is available at "https://www.youtube.com/embed/IAX8-wOgImc?si=CdC_gDJQmBnrNGEq" 

####  Step 2 : Import data and manage server
* A quick youtube video link is available at "https://www.youtube.com/embed/9Js5P2Gn_nk?si=7tnBI5l4xqypNcmh"


####  Step 3 : Find peaks and max peak values
* A quick youtube video link is available at "https://www.youtube.com/embed/3bl7pVS2CWI?si=Zdvoku9h_T1JQkfG" 


####  Step 4 : Finding orientation matrix
* A quick youtube video link is available at "https://www.youtube.com/embed/AKL9SOP9clQ?si=BmiP6PhG6uTt3T8u" 


####  Step 5 : Check HKLI 
* A quick youtube video link is available at "https://www.youtube.com/embed/qbSChMwf0Ck?si=4oNTPcOg9_gqFA2p" 


####  Step 6 : Check data : HKLI Volume
* A quick youtube video link is available at "https://www.youtube.com/embed/5_G1QN8JlMw?si=CckLYZPVJmbeBffS" 

####  Step 7 : Parent file selection for processing different temperatures datasets
* Check the data
* Make sure data looks good 
* Select the file as the parent file
* A quick youtube video link is available at "https://www.youtube.com/embed/dCsU3QN5yQ0?si=56-IMaUNto7gdNBh" 


####  Step 8 : Check the viewing server log
* A quick youtube video link is available at "https://www.youtube.com/embed/EwwbVRqq308?si=u0m6DHsAH_AgnnOb" 





---



# nxrefine_General_Node.md

# NXRefine
The code is written by Dr. Ray Osborn. More details will be available [NXRefine](https://nexpy.github.io/nxrefine/).The code provides various tools for stacking the raw data, finding Bragg peaks, solving the orientation matrix, and finally providing the HKL. 


# Data Policy 
We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.

# NXRefine General Nodes
(https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Beamline%20computers.png?raw=true)

* Step 1 :

 Make sure you have permission for the desired folders,  before running the job in the queue, ask your beamline scientist to change the permission of the folder (it is always need to be updated). Also, make sure you have the parent file for each folders, otherwise the code will not work. Change the <classe_id> to your own CLASSE ID

* Step 2 : Login to lnx201
ssh <classe_id>@lnx201.classe.cornell.edu

* Step 3 : 
qrsh -q interactive.q -l mem_free=350G -pe sge_pe 20

* Step 4 : Go to the desired data analayis forder (it will your folder in aux)
cd /nfs/chess/id4baux/2024-1/<BTR-3946-a>/

* Step 5 :: 
a. Changed the desired steps for nxrefine from the folder or if you know how to use vim, then do to change the qsub file and do that necessasy steps 
b. Make sure you have change the file path and the threshold of the nxfind of the sample
c. If you are nomachine, you can change the qsub_jobs_****.sh file directly based on the steps you want to perform in the data processing  
vim qsub_jobs_<name of the user>.sh 

* Step 6 : Run the job in lnx201 (make sure path is correct)
qsub -q all.q -l mem_free=350G -pe sge_pe 32 /nfs/chess/id4baux/2025-1/sarker-3946-a/qsub_jobs_<name of the file>.sh
"If it did not work, try to use less memory and submit the job again" 

* Step 7 : You can change mem_free = 200, below is the example
qsub -q all.q -l mem_free=200G -pe sge_pe 32 /nfs/chess/id4baux/2025-1/sarker-3946-a/qsub_jobs_<name of the file>.sh

* Step 8 : Check the status using the command "qstat"

* Step 9 : See the status ebaborately
cat qsub_jobs_<classe_id>.sh.e7231424

* Step 10 : Finally after you the data procesing
chmod -R 777 /nfs/chess/id4baux/2025-1/<project_name>
        For Example: 
        chmod -R 777 /nfs/chess/id4baux/2025-1/sarker-3490-a

## To reprocess the data with higher step size or better resolution:
 
!!! hint "Reprocessing steps"

    Once you have received the HKLI data from the QM2 beamline, you can visualize the data. If you want higher resolution in nxrefine trnasform stage and nxcombine you can modify that. Below is the help command to see what paramters you can change in `nxtransform` and `nxcombine` stage.


        nxtransform --h
        usage: nxtransform [-h] -d DIRECTORY [-e ENTRIES [ENTRIES ...]] [-qh QH QH QH] [-qk QK QK QK] [-ql QL QL QL] [-R] [-M] [-o] [-q]
        Perform CCTW transform options:
        -h, --help show this help message and exit
        -d DIRECTORY, --directory DIRECTORY scan directory
        -e ENTRIES [ENTRIES ...], --entries ENTRIES [ENTRIES ...] names of entries to be processed
        -qh QH QH QH Qh - min, step, max
        -qk QK QK QK Qk - min, step, max
        -ql QL QL QL Ql - min, step, max
        -R, --regular perform regular transform
        -M, --mask perform transform with 3D mask
        -o, --overwrite overwrite existing transforms
        -q, --queue add to server task queue


        nxcombine --h
        usage: nxcombine [-h] [-d DIRECTORY] [-e ENTRIES [ENTRIES ...]] [-R] [-M] [-o] [-q]

        Combine CCTW transforms

        options:
        -h, --help            show this help message and exit
        -d DIRECTORY, --directory DIRECTORY
                                scan directory
        -e ENTRIES [ENTRIES ...], --entries ENTRIES [ENTRIES ...]
                                names of entries to be combined.
        -R, --regular         combine transforms
        -M, --mask            combine transforms with 3D mask
        -o, --overwrite       overwrite existing transform
        -q, --queue           add to server task queue

Now based on the `help` command, you can modify the script and add the `min` `stepsize` `max` for your desired data. For example, previously your HKLI and step size is below
(https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/transform.png?raw=true)
However, you want to change that. To modify, you go your previous script and add `min` `stepsize` `max` in `nxtransform`.   
I’ve provided an example of the script for general node lnx201. For clarity, I used the full path but you may want to modify it based on your directory structure and desired parameter values. Also, note that instead of using `nxreduce`, this workflow separates the process into two steps: `nxtransform` and `nxcombine`. In both cases, it is important that you `overwrite` the exsisting data.

!!! hint "Modification of the script"

### To modify the script:
Step 1: Comment out the below line
#nxreduce --directory ${USER_DIR}${TEMP} --entries f1 f2 f3 --transform --combine --regular

Step 2: Add and modify below 
nxtransform --directory /nfs/chess/id4baux/2023-3/sarker-3828-a/nxrefine/AB3C5/sample1/16/ --entries f1 f2 f3 -qh -8 0.01 8 -qk -8 0.01 8 -ql -18 0.01 18 --regular --overwrite

Step 3: Finally combine
nxcombine --directory /nfs/chess/id4baux/2023-3/sarker-3828-a/nxrefine/AB3C5/sample1/16/ --entries f1 f2 f3 --regular --overwrite

Step 4: After getting the data, visulize the HKLI and once you are satified with the stepsize, you set that as `parent file` again and reprocess rest of the dataset.


---



# publications.md

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Research%20area.png?raw=true){ width="800" }
</figure>

## List of publications - Quantum Materials Beamline
(please click the paper to see the details - this list is not complete)

## 2025

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2025-v1.png?raw=true){ width="700" }
</figure>


1. [Dongliang Gong, Junyi Yang, Shu Zhang, Shashi Pandey, Dapeng Cui, Jacob PC Ruff, Lukas Horak et al. "Large asymmetric anomalous Nernst effect in the antiferromagnet SrIr0. 8Sn0. 2O3." Nature Communications 16, no. 1 : 2888 (2025)](https://www.nature.com/articles/s41467-025-58020-0)

2. [Zhong-Zhen Luo, Hengdi Zhao, Weizhao Cai, Shima Shahabfar, Juncen Li, Songting Cai, Jameson Berg et al. "Charge Density Wave and Superconductivity in BaSbTe2S Heterolayer Crystal with 2D Te Square Nets." Journal of the American Chemical Society (2025).](https://pubs.acs.org/doi/full/10.1021/jacs.4c16505)

3. [J. J. Huang, Y. Yang, D. Weinstock, C. R Bundschu, Q. Li, S. Sarker, J. PC Ruff, T.A. Arias, H. D Abruña, A. Singer, "Multimodal in situ X-ray mechanistic studies of a bimetallic oxide electrocatalyst in alkaline media." Nature Catalysis 1-10 (2025)](https://www.nature.com/articles/s41929-025-01289-7)

4. [S. Li, D. Chen, B. Li, H. Yan, B. J Lawrie, B. Choi, D. Rhee, Y. Li, H. Zhao, L. Chen, A. Pattammattel, S. Sarker, D. Jariwala, P. Guo, "Spontaneous Formation of Single-Crystalline Spherulites in a Chiral 2D Hybrid Perovskite." Journal of the American Chemical Society (2025)](https://pubs.acs.org/doi/full/10.1021/jacs.4c15471)

5. [S. Hazra, T. Schwaigert, A. Ross, H. Lu, U. Saha, V. Trinquet, B. Akkopru‐Akgun, B. Z Gregory, A. Mangu, S. Sarker, T. Kuznetsova, S. Sarker, X. Li, M. R Barone, X. Xu, J. W Freeland, R. Engel‐Herbert, A. M Lindenberg, A. Singer, S. Trolier‐McKinstry, D. A Muller, G‐M Rignanese, S. Salmani‐Rezaie, V. A Stoica, A. Gruverman, L‐Qing Chen, D. G. Schlom, V. Gopalan, "Colossal Strain Tuning of Ferroelectric Transitions in KNbO3 Thin Films." Advanced Materials 36, 52, 2408664 (2025)](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adma.202408664)

## 2024

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2024-lit1.png?raw=true){ width="700" }
</figure>


6. [B. R. Ortiz, W. R Meier, G. Pokharel, J. Chamorro, F. Yang, S. Mozaffari, A. Thaler, S. J. Gomez Alvarado, H. Zhang, D. S. Parker, G. D.  Samolyuk, J. AM Paddison, J. Yan, F. Ye, S. Sarker, S. D. Wilson, H. Miao, D. Mandrus, M. A. McGuire, "Stability Frontiers in the AM 6 X 6 Kagome Metals: The Ln Nb6Sn6 (Ln: Ce–Lu, Y) Family and Density-Wave Transition in LuNb6Sn6." Journal of the American Chemical Society (2024)](https://pubs.acs.org/doi/full/10.1021/jacs.4c16347)

7. [Chandrashekhar P.Savant,  Anita Verma, Thai-Son Nguyen, Len van Deurzen, Yu-Hsin Chen, Zhiren He, Salva S. Rezaie, S. Sarker, J.Ruff, "Self-activated epitaxial growth of ScN films from molecular nitrogen at low temperatures." APL Materials 12, 11 (2024)](https://pubs.aip.org/aip/apm/article/12/11/111108/3319133)

8. [N. Derimow, J T Benzing, H. Joress, A. McDannald, P. Lu, F. W DelRio, N. Moser, M. J Connolly, A. Saville, O. L Kafka, C. Beamer, R. Fishel, S. Sarker, C. Hadley, N. Hrabe, “Microstructure and mechanical properties of laser powder bed fusion Ti-6Al-4V after HIP treatments with varied temperatures and cooling rates.” Materials & Design, 113388 (2024)](https://www.sciencedirect.com/science/article/pii/S0264127524007639)

9. [S. Gomez, G. Pokharel, B. R. Ortiz, J. AM Paddison, S. Sarker, J. P. C. Ruff, and S. D. Wilson. "Frustrated Ising charge correlations in the kagome metal ScV6Sn6." Physical Review B, 110(14), L140304 (2024)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.110.L140304)

10. [J. Plumb, A. C. Salinas, K. Mallayya, E. Kisiel, F. B Carneiro, R. Gomez, G. Pokharel, Eun-Ah Kim, S. Sarker, Z. Islam, S. Daly, S. D. Wilson, "Phase-separated charge order and twinning across length scales in CsV3Sb5." Physical Review Materials 8,9 093601 (2024)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.8.093601)

11. [ Haozhe Wang, Alberto de la Torre, Joseph T Race, Qiaochu Wang, Jacob PC Ruff, Patrick M Woodward, Kemp W Plumb, David Walker, Weiwei Xie,Pseudosymmetry in Tetragonal Perovskite SrIrO3 Synthesized under High Pressure." ACS Applied Electronic Materials 6, no. 9 (2024): 6820-6825](https://pubs.acs.org/doi/full/10.1021/acsaelm.4c01214)

12. [ S B Lee, J. S Van Buskirk, F. Katmer, S. Sarker, D. C Fredrickson, L. M Schoop, “Polymorphism within the Quasi-One-Dimensional Au2MP2 (M= Tl, Pb, Pb/Bi, and Bi) Series”, Chemistry of Materials, 36(17), 8217-8228 (2024)](https://pubs.acs.org/doi/full/10.1021/acs.chemmater.4c00784)

13. [Subin Kim, Ezekiel Horsley, Jacob PC Ruff, Beatriz D Moreno, Young-June Kim,  "Structural transition and magnetic anisotropy in α-RuCl 3." Physical Review B 109, no. 14 L140101 (2024)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.109.L140101)

14. [Wu, Han, Lei Chen, Paul Malinowski, Bo Gyu Jang, Qinwen Deng, Kirsty Scott, Jianwei Huang et al. "Reversible non-volatile electronic switching in a near-room-temperature van der Waals ferromagnet." Nature Communications 15, no. 1 2739 (2024)](https://www.nature.com/articles/s41467-024-46862-z)

15. [S. Li, X. Xu, C.A. Kocoj, C. Zhou, Y. Li, D. Chen, J.A. Bennett, S. Liu, L. Quan, S. Sarker, and Liu, M.” Large exchange-driven intrinsic circular dichroism of a chiral 2D hybrid perovskite”. Nature Communications, 15(1), 2573 (2024)](https://www.nature.com/articles/s41467-024-46851-2)

16. [R. Singha, F, Yuan, S.B. Lee, G.V. Villalpando, G. Cheng, B. Singh, S. Sarker, N. Yao, K.S. Burch, and L.M. Schoop, “Anisotropic and High‐Mobility Electronic Transport in a Quasi 2D Antiferromagnet NdSb2”. Advanced Functional Materials, 34(10), p.2308733 (2024)](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adfm.202308733)

## 2023

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2023-lit2.png?raw=true){ width="800" }
</figure>



17. [Cheng Chen, Weichen Tang, Xiang Chen, Zhibo Kang, Shuhan Ding, Kirsty Scott, Siqi Wang et al. "Anomalous excitonic phase diagram in band-gap-tuned Ta2Ni (Se, S) 5." Nature Communications 14, no. 1: 7512 (2023)](https://www.nature.com/articles/s41467-023-43365-1)

18. [Pokharel, Ganesh, Brenden R. Ortiz, Linus Kautzsch, S. J. Gomez Alvarado, Krishnanand Mallayya, Guang Wu, Eun-Ah Kim, Jacob PC Ruff, Suchismita Sarker, and Stephen D. Wilson. "Frustrated charge order and cooperative distortions in ScV 6 Sn 6." Physical Review Materials 7, no. 10: 104201 (2023)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.7.104201)

19. [Ortiz, Brenden R., Ganesh Pokharel, Malia Gundayao, Hong Li, Farnaz Kaboudvand, Linus Kautzsch, Suchismita Sarker et al. "Erratum: YbV 3 Sb 4 and EuV 3 Sb 4 vanadium-based kagome metals with Yb 2+ and Eu 2+ zigzag chains [Phys. Rev. Materials 7, 064201 (2023)]." Physical Review Materials 7, no. 9 099901 (2023)](https://journals.aps.org/prmaterials/pdf/10.1103/PhysRevMaterials.7.099901)

20. [Kautzsch, Linus, Yuzki M. Oey, Hong Li, Zheng Ren, Brenden R. Ortiz, Ganesh Pokharel, Ram Seshadri et al. "Incommensurate charge-stripe correlations in the kagome superconductor CsV3Sb5− x Sn x." npj Quantum Materials 8, no. 1 37 (2023)](https://www.nature.com/articles/s41535-023-00570-x)

21. [Xiang Chen, Wei Tian, Yu He, Hongrui Zhang, Tyler L. Werner, Saul Lapidus, Jacob PC Ruff, Ramamoorthy Ramesh, and Robert J. Birgeneau. "Thermal cycling induced alteration of the stacking order and spin-flip in the room temperature van der Waals magnet Fe 5 GeTe 2." Physical Review Materials 7, no. 4 044411 (2023)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.7.044411)

22. [Linus Kautzsch, Brenden R Ortiz, Krishnanand Mallayya, Jayden Plumb, Ganesh Pokharel, Jacob PC Ruff, Zahirul Islam, Eun-Ah Kim, Ram Seshadri, Stephen D Wilson, "Structural evolution of the kagome superconductors AV 3 Sb 5 (A= K, Rb, and Cs) through charge density wave order." Physical Review Materials 7, no. 2 024806 (2023)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.7.024806)

23. [Stephen Wilson, Linus Kautzsch, Yuzki Oey, Hong Li, Zheng Ren, Brenden Ortiz, Ganesh Pokharel et al. "Incommensurate charge-stripe correlations in the kagome superconductor CsV3Sb5-xSnx." (2023)](https://web.archive.org/web/20230125063048id_/https://assets.researchsquare.com/files/rs-2490447/v1/88ab56684adabf3a5fb9823f.pdf?c=1674628127)

24. [Ramette, Caleb, Lucas Pressley, Maxim Avdeev, Minseong Lee, Satya Kushwaha, Matthew Krogstad, Suchismita Sarker et al. "Floating zone crystal growth, structure, and properties of a cubic Li 5.5 La 3 Nb 1.5 Zr 0.5 O 12 garnet-type lithium-ion conductor." Journal of Materials Chemistry A 11, no. 40 21754-21766 (2023)](https://pubs.rsc.org/en/content/articlehtml/2023/ta/d3ta04606k)

25. [Shao, Ziming, Noah Schnitzer, Jacob Ruf, Oleg Yu Gorobtsov, Cheng Dai, Berit H. Goodge, Tiannan Yang et al. "Real-space imaging of periodic nanotextures in thin films via phasing of diffraction data." Proceedings of the National Academy of Sciences 120, no. 28 e2303312120 (2023)](https://www.pnas.org/doi/pdf/10.1073/pnas.2303312120)


## 2022

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2022_lit1.png?raw=true){ width="700" }
</figure>



25. [Ganesh Pokharel, Brenden Ortiz, Juan Chamorro, Paul Sarte, Linus Kautzsch, Guang Wu, Jacob Ruff, Stephen D Wilson,  "Highly anisotropic magnetism in the vanadium-based kagome metal TbV 6 Sn 6." Physical Review Materials 6, no. 10 104202(2022)](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.104202)

26. [Tsung-Han Yang, S Kawamoto, Tomoya Higo, SuYin Grass Wang, MB Stone, Joerg Neuefeind, Jacob PC Ruff, AM Milinda Abeykoon, Yu-Sheng Chen, S Nakatsuji, and KW Plumb. "Bond ordering and molecular spin-orbital fluctuations in the cluster Mott insulator GaTa4Se8." Phys. Rev. Research 4, 033123 (2022)](https://doi.org/10.1103/PhysRevResearch.4.033123)

27. [Linus Kautzsch, Yuzki M Oey, Hong Li, Zheng Ren, Brenden R Ortiz, Ram Seshadri, Jacob Ruff, Ziqiang Wang, Ilija Zeljkovic, and Stephen D Wilson. “Incommensurate charge-stripe correlations in the kagome superconductor CsV3Sb5−xSnx” arXiv:2207.10608 (2022)](https://doi.org/10.48550/arXiv.2207.10608) 

28. [Jordan Venderley, Krishnanand Mallayya, Michael Matty, Matthew Krogstad, Jacob Ruff, Geoff Pleiss, Varsha Kishore, David Mandrus, Daniel Phelan, Lekhanath Poudel, Andrew Gordon Wilson, Kilian Weinberger, Puspa Upreti, Michael Norman, Stephan Rosenkranz, Raymond Osborn, and Eun-Ah Kim. “Harnessing interpretable and unsupervised machine learning to address big data from modern X-ray diffraction.” PNAS 119, 24, e2109665119 (2022)](https://doi.org/10.1073/pnas.2109665119)

29. [Ganesh Pokharel, Brenden Ortiz, Paul Sarte, Linus Kautzsch, Guang Wu, Jacob Ruff, and Stephen D Wilson. “Highly anisotropic magnetism in the vanadium-based kagome metal TbV6Sn6.” arXiv:2205.15559 (2022)](https://doi.org/10.48550/arXiv.2205.15559)

30. [Cheng Chen, Xiang Chen, Weichen Tang, Zhenglu Li, Siqi Wang, Shuhan Ding, Chris Jozwiak, Aaron Bostwick, Eli Rotenberg, Makoto Hashimoto, Donghui Lu, Jacob PC Ruff, Steven G Louie, Robert Birgeneau, Yulin Chen, Yao Wang, and Yu He. “Lattice fluctuation induced pseudogap in quasi-one-dimensional Ta2NiSe5.”arXiv:2203.06817 (2022)](https://doi.org/10.48550/arXiv.2203.06817)

31. [Jason J Huang, Daniel Weinstock, Hayley Hirsh, Ryan Bouck, Minghao Zhang, Oleg Yu Gorobtsov, Malia Okamura, Ross Harder, Wonsuk Cha, Jacob PC Ruff, Y Shirley Meng, and Andrej Singer. “Disorder Dynamics in Battery Nanoparticles During Phase Transitions Revealed by Operando Single-Particle Diffraction.” Adv. Energy Mater. 12, 2103521 (2022).](https://doi.org/10.1002/aenm.202103521)

32. [Lv, B. Q., Alfred Zong, D. Wu, A. V. Rozhkov, Boris V. Fine, Su-Di Chen, Makoto Hashimoto et al. "Unconventional hysteretic transition in a charge density wave." Phys. Rev. Lett. 128, 3, 036401 (2022).](https://doi.org/10.1103/PhysRevLett.128.036401)

33. [S. Sharma, M. Pocrnic, B. N. Richtik, C. R. Wiebe, J. Beare, J. Gautreau, J. P. Clancy, J. P. C. Ruff, M. Pula, Q. Chen, S. Yoon, Y. Cai, and G. M. Luke. “Synthesis and physical and magnetic properties of CuAlCr4S8: A Cr-based breathing pyrochlore.” Phys. Rev. B 106, 024407 (2022)](https://doi.org/10.1103/PhysRevB.106.024407)

## 2021


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2021.png?raw=true){ width="700" }
</figure>



34. [Daniel Weinstock, Hayley S Hirsh, Oleg Yu Gorobtsov, Minghao Zhang, Jason Huang, Ryan Bouck, Jacob PC Ruff, Y Shirley Meng, and Andrej Singer. “Structure-selective operando x-ray spectroscopy.” ACS Energy Letters 7, 1, 261–266 (2021)](https://doi.org/10.1021/acsenergylett.1c02371)

35. [Brenden R Ortiz, Samuel ML Teicher, Linus Kautzsch, Paul M Sarte, Noah Ratcliff, John Harter, Jacob PC Ruff, Ram Seshadri, and Stephen D Wilson. "Fermi surface mapping and the nature of charge density wave order in the kagome superconductor CsV3Sb5." Phys. Rev. X 11, 041030 (2021).](https://doi.org/10.1103/PhysRevX.11.041030)

36. [Xu, Su-Yang, Qiong Ma, Yang Gao, Anshul Kogar, Alfred Zong, Andrés M. Mier Valdivia, Thao H. Dinh et al. "Spontaneous gyrotropic electronic order in a transition-metal dichalcogenide." Nature 578, no. 7796 545-549 (2020)](https://doi.org/10.1038/s41586-020-2011-8)

37. [Antonio, Daniel J., Joel T. Weiss, Katherine S. Shanks, Jacob PC Ruff, Marcelo Jaime, Andres Saul, Thomas Swinburne et al. "Piezomagnetic switching and complex phase equilibria in uranium dioxide." Communications Materials 2, no. 1  1-6 (2021):](https://doi.org/10.1038/s43246-021-00121-6)

38. [Lee, Jooseop, Karel Prokeš, Sohee Park, Igor Zaliznyak, Sachith Dissanayake, Masaaki Matsuda, Matthias Frontzek et al. "Charge density wave with anomalous temperature dependence in UPt2Si2." Physical Review B 102, no. 4 041112 (2020)](https://doi.org/10.1103/PhysRevB.102.041112) 

39. [Jiang, Yu-Xiao, Jia-Xin Yin, M. Michael Denner, Nana Shumiya, Brenden R. Ortiz, Gang Xu, Zurab Guguchia et al. "Unconventional chiral charge order in kagome superconductor KV3Sb5." Nature Materials,  1-5 (2021)](https://doi.org/10.1038/s41563-021-01034-y)

40. [Ghale, Purnima. "Energy of non-relativistic many-particle quantum states from non-commuting Coulomb field and momentum operators. (2021)](https://arxiv.org/abs/2010.01656)

41. [Shi, Zhenzhong, S. J. Kuhn, F. Flicker, T. Helm, J. Lee, William Steinhardt, Sachith Dissanayake et al. "Incommensurate two-dimensional checkerboard charge density wave in the low-dimensional superconductor Ta4Pd3Te16." Physical Review Research 2, no. 4  042042 (2020)](https://doi.org/10.1103/PhysRevResearch.2.042042)

42. [Thedford, R. Paxton, Peter A. Beaucage, Ethan M. Susca, Corson A. Chao, Katja C. Nowack, Robert B. Van Dover, Sol M. Gruner, and Ulrich Wiesner. "Superconducting Quantum Metamaterials from High Pressure Melt Infiltration of Metals into Block Copolymer Double Gyroid Derived Ceramic Templates." Advanced Functional Materials 31, no. 23  2100469 (2021)](https://doi.org/10.1002/adfm.202100469)

43. [Chen, Xiang, Yu He, Shan Wu, Yu Song, Dongsheng Yuan, Edith Bourret-Courchesne, Jacob PC Ruff, Zahirul Islam, Alex Frano, and Robert J. Birgeneau. "Structural and magnetic transitions in the planar antiferromagnet Ba4Ir3O10." Physical Review B 103, no. 22 224420 (2021)](https://doi.org/10.1103/PhysRevB.103.224420)

## 2020

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/2020.png?raw=true){ width="700" }
</figure>


44. [Reig-i-Plessis, D., T. A. Johnson, K. Lu, Q. Chen, J. P. C. Ruff, M. H. Upton, T. J. Williams et al. "Structural, electronic, and magnetic properties of nearly ideal Jeff= 1/2 iridium halides." Physical Review Materials 4, no. 12 124407 (2020)](https://doi.org/10.1103/PhysRevMaterials.4.124407)

45. [Gadkari, D., K. S. Shanks, H. T. Philipp, M. W. Tate, J. Thom-Levy, and S. M. Gruner. "Characterization of an architecture for front-end pixel binning in an integrating pixel array detector." Journal of Instrumentation 15, no. 11 T11002 (2020) ](http://doi.org/10.1088/1748-0221/15/11/T11002)

46. [Su-Yang Xu,Qiong Ma, Yang Gao, Anshul Kogar, Alfred Zong, Andrés M. Mier Valdivia, Thao H. Dinh et al. "Spontaneous gyrotropic electronic order in a transition-metal dichalcogenide." Nature 578, no. 7796 545-549 (2020)](https://www.nature.com/articles/s41586-020-2011-8)

47. [Lee, Jooseop, Karel Prokeš, Sohee Park, Igor Zaliznyak, Sachith Dissanayake, Masaaki Matsuda, Matthias Frontzek et al. "Charge density wave with anomalous temperature dependence in UPt 2 Si 2." Physical Review B 102, no. 4 041112 (2020)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.102.041112)

50. [Zhenzhong Shi, S. J. Kuhn, F. Flicker, Toni Helm, J. Lee, William Steinhardt, Sachith Dissanayake et al. "Incommensurate two-dimensional checkerboard charge density wave in the low-dimensional superconductor Ta 4 Pd 3 Te 16." Physical Review Research 2, no. 4 042042 (2020)](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.2.042042)

## Ph.D Thesis - Quantum Materials Beamline

#### 2024
1. [Subin Kim, Structural and Magnetic Properties of α-RuCl3 Single Crystal, 2024](https://www.proquest.com/docview/3125860926?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses)

2. [Farnaz Kaboudvand, Electronic instability in the kagome materials, 2024 ](https://www.proquest.com/docview/3123652387?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses)

#### 2023

3. [CT Parzyck, Synthesis, Characterization, and Scattering Measurements of the Perovskite and Infinite Layer Nickelates, 2023](https://www.proquest.com/docview/2916340139?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses)

4. [S Sharma, Study of unconventional superconductors and breathing pyrochlore magnets, 2023 ](https://macsphere.mcmaster.ca/handle/11375/28730)

#### 2022

5. [Amani Jayakody, Cubic Perovskite Materials with Quantum Properties: Effect of Strain Quantum Phase Transition, and Electronic/Magnetic Phase Separation, 2022](https://www.proquest.com/docview/3073211469?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses)

6. [Yuzki Mizutani Oey,Structural Effects and Compositional Tuning in Magnetocalorics and Kagome Superconductors,2022](https://www.proquest.com/docview/2776968023?pq-origsite=gscholar&fromopenview=true&sourcetype=Dissertations%20&%20Theses)




---



# pymca.md


# PyMca

[PyMca](http://pymca.sourceforge.net/index.html) is developed by European Synchrotron Radiation Facility (ESRF). You can visulize and analyze the  energy-dispersive X-ray fluorescence data. It access SPEC shared memory to monitor data acquisation. The user can see their plots in pyMCA. 

For more information visit [PyMca website]( http://pymca.sourceforge.net/index.html)  





---



# sample.md


The procedure of mounting/changing the sample depends on the type of experiment performed ID4B.


### Single-crystal mounts

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sample_mount.png?raw=true){ width="600" }
</figure>

*  Step 1 : 
a. You need goniometer-bases 
b. link for the base : B5 (SPINE Style) Goniometer Bases is [SKU: GB-B5-R-20](https://www.mitegen.com/product/b5-spine-style-goniometer-bases/)

*  Step 2 : 
a. Micromount : MiTeGen is used for micromount pin. It is composed of thin polymer tips attached to beveled non-magnetic 0.025″ (0.64 mm) diameter stainless steel rods (pins).
b. The link for the sample tip is [SKU: M2-L18SP-100](https://www.mitegen.com/product/dual-thickness-micromounts/) and the aperture Size is 100 μm.

*  Step 3 : Do not touch the tips with your hands. Always use tweezers along the pin shaft, not the tip.
*  Step 4 : 
a. Use GE vernish to glue the micromount to base 
b. The link for Adhesive [VGE -7031](https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-accessories/varnish)

*  Step 5 : Make sure you do not touch the metal part with the sample!!


### Few other accessories to to handle small samples: 

* [Cryo Vials](https://www.mitegen.com/product/magnetic-cryovials/)
* [Magnetic Wand](https://www.mitegen.com/product/magnetic-wand-with-rubber-grips/)


### Thin-film mounts

*  Step 1 : 
a. You need goniometer-bases 
b. link for the base : B5 (SPINE Style) Goniometer Bases at https://www.mitegen.com/product/b5-spine-style-goniometer-bases/

*  Step 2 : 
a. Fiber glass  
b. Example fiberglass link at https://www.amazon.com/Piece-Fiberglass-Solid-Blank-Inches/dp/B0052TVI0K/

*  Step 3 : 
a. Adhesive  
b. Example adhesive link used at CHESS: https://www.lakeshore.com/products/categories/specification/temperature-products/cryogenic-accessories/varnish


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/thin-film%20samples1.png?raw=true){ width="500" }
</figure>

# Sample shipment details 

If you want to send the samples to CHESS, please follow the [instructions here](https://www.chess.cornell.edu/users/shipping)


# Air sensitive samples

If coating needed, one of the example could be (https://www.agc-chemicals.com/jp/en/fluorine/products/detail/index.html?pCode=JP-EN-F019#:~:text=CYTOP%C2%AE%20is%20a%20fluoropolymer,coat%2C%20and%20more%20are%20possible)



---



# sample_alignment_HDRM.md

# Welcome to CHESS &#60QM&#62<sup>2</sup> Sample Alignment


![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/beamline.jpeg?raw=true){ width="300" }

!!! danger "High Dynamic Range Reciprocal Space Mapping (HDRM)"


#### Basic Theory - HDRM

High Dynamic Range Mapping (HDRM) is primarily a method for studying single crystal samples, although it can also be effective for studying thin films. HDRM aims is to rapidly study wide regions of reciprocal space, collecting the intense Bragg peaks required to refine crystal structures along with weak features associated with superstructures, and the slowly modulated scattering associated with phonons and short-range order[[1](https://www.chess.cornell.edu/srn-article-cartography-7-dimensions-chess)].

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/goniometer1.png?raw=true){ width="150" }
</figure>

!!! hint "Single Crytal Alignment"
      Basic steps for single crystal sample alignment - HDRM

## BASIC STEPS FOR SINGLE CRYSTAL SAMPLE ALIGNMENT - HDRM
For Manually stage: 
            center the sample to the beam 
            FOURC> umvr samz2 0.1 (relative motion of the sample movement up (+) and down (-)) 
            FOURC> umv phi2 0
            FOURC> umv phi2 180
            Move x and y to make the sample to the cursor
            FOURC> umv phi2 90
            FOURC> umv phi2 270
            Do it iteratively until the center of the axis match the sample position   



!!! danger "Carefully and slowly insert the sample in the top of the sample stage"

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Qm2%20sample%20stage.png?raw=true){ width="450" }
</figure>


## STEPS for Automated stage: 
# Step 1:
            center the sample to the beam 
            FOURC> umvr samz 0.1 (relative motion of the sample movement up (+) and down (-)) 
            FOURC> umv phi 0
            FOURC> umvr samx 0.1 (make sure you can see sample is moving towards cross +)
            FOURC> umv phi 180 (check the sample is coming back to cross + )
            Move x and y to make the sample to the cursor
            FOURC> umv phi 90
            FOURC> umvr samy 0.1 (make sure you can see sample is moving towards cross +)
            FOURC> umv phi 270 (check the sample is coming back to cross + )

            Do it iteratively until the center of the axis match the sample position     

#  Step 2 :  Create file structure 
a. Create newfile as FOURC>newfile <samplename> 
b. samplename : chemical name of your sample, make sure you created folder in your directory
c. Open HDRMscans.mac script and sort your path (sortmypathout)
d. Change the _mysample = <sample_identifier> where _mysample is the sample identifier
e. save the file


!!! danger "check the signals"



#  Step 3: Run HDRMscans.mac script from terminal 
 a. FOURC> qdo ./HDRMscans.mac  Notes: HDRMscans.mac contains all the script



#  Step 4 : If you want to check the best height for the sample (finding smaller sample best position) 
a. FOURC>heightscan 
b. Data will save at 'tiff' folder inside the user folder at id4b
c. Check the quality of the datasets at nexpy
d. Go to the best position of the sample using FOURC> umv samz <position of the sample>  

# Step 5 : Autotune condition (talk to beamline scientist)  
If the autotune is off in the mostab
a. FOURC> opens (# Open the shutter)
b. Turn the knob slowly and maximize the counts in IC2
c. FOURC> closes (# close the shutter)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/mostab.png?raw=true){ width="150" }
</figure>


# Step 6: Run three rotation crystal scan 
a. It will rotate the crystal three times at different chi and theta angle
FOURC> threextalscan 300 1 
b. #Notes: In the threextalscan 1st parameter is temperature 300K and the second parameter is waiting time 1 min
c. It will vary chi, theta and phi angle
d. Collect data phi 0-365 with 3650 images (1 degree/frame)
e. You can the change the exposure time (if needed)
f. Data will save at raw6M in id4b folder

#### Quick video on data collection (make sure you read the above instructions before watching the video)
at "https://www.youtube.com/embed/qsAZLayF4Ow?si=oIitQSArHTU1FunV"


#  Step 7: Check data nexpy  
Please look at the [Data visualization](https://suchismitasarker.github.io/CHESS-ID4B-QM2/nexpy/ ) - Nexpy section

=============================================================================

!!! type "Temperature modify and collect data"

##  Changing temperature from 300K and 90 K- (if you are at Nitrogen atomosphere)
a. FOURC> te 100 # note: temperature here is 100 Kelvin
b. Make sure the temperature is stable before you run script
c. FOURC> threextalscan 100 1 
d. For practical guide of the temperature switch between nitrogen and helium, click the link for details (https://suchismitasarker.github.io/CHESS-ID4B-QM2/temp/)


!!! hint "Thin-film Alignment"

## THIN-FILM ALIGNMENT
Basic steps for single crystal thin-film sample alignment - HDRM. Detector height needs to change because of grazing incidence. Make sure you are able to see the samples (proper light arrangements)

# Step 1:  
a. Center the sample to the beam 
b. Move chi, phi, and theta positions to their initial setup
FOURC> umv chi 90   
FOURC> umv phi 0  
FOURC> umv th 0  
c. Perform height adjustment by: 
Check the signal at the diode 
FOURC> tw samz 0.01
Move the sample in the Z-directions and cut the beam in half (for example: if the beam size is 300 microns, move 150 microns from the surface when the signal goes down)            
d. Place cursor at center of the sample 
FOURC> umv phi 0
FOURC> umv phi 180
FOURC> umv phi 90
FOURC> umv phi 270

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/signals1.png?raw=true){ width="500" }
</figure>

# Step 2 :  
a. Creating the file structure
b. Create newfile : FOURC>newfile samplename
c. Open HDRMscans.mac script for thin-film
d. Change the sample ID

# Step 3: 
a. Run HDRMscans.mac script from terminal
b. FOURC> qdo ./HDRMscans.mac #Notes:HDRMscans.mac contains all the script


# Step 4: 
a. Check the best height for the sample it will generate tiff file
b. FOURC>powderscan 300 1
c. Check the quality of the data sets at nexpy
d. Go to the best position of the sample

# Step 5: 
a. Autotune condition (talk to beamline scientist)

## If the autotune is off in the mostab
a. FOURC> opens (# Open the shutter)
b. Turn the knob slowly and maximize the counts in IC2
c. FOURC> closes (# close the shutter)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/mostab.png?raw=true){ width="150" }
</figure>

# Step 6: 
a. Run three rotation crystal scan 
b. FOURC> threxstalscan 300 1 #Notes: Parameters: Temperature = 300, Sleep = 1

# Step 7: 
a. Check data nexpy 
b. (please look at the Data visulization - Nexpy section )


### Examples of Temperature Dependent Scans 

## Temperature Dependent scan: 300K- 475K at 25K temperature interval

# Steps: 
a. Follow the instruction of temprature switch 300K-500K and the temperature to stabilize

def TScans_high_N2 '
te = 325
for (loopT=325; loopT<476; loopT=loopT+25){
eval(sprintf("threextalscan %s 180",loopT))
}

'
## Temperature Dependent scan: 90K- 300K at 25K temperature interval
def Tscans_low_to_high_N2 '
for (loopT=90; loopT < 301; loopT=loopT+15){
eval(sprintf("threextalscan %s 180", loopT))
}
'

## Temperature Dependent scan: 90K- 100K at 2K temperature interval, 100K-126K at 5K interval and 125K-200K at 25K interval
def HighTScans_different_range '
for (loopT=90; loopT < 101; loopT=loopT+2){
eval(sprintf("threextalscan_longexposure %s 180", loopT))
}

for (loopT=100; loopT < 126; loopT=loopT+5){
eval(sprintf("threextalscan_longexposure %s 180", loopT))
}

for (loopT=125; loopT < 200; loopT=loopT+25){
eval(sprintf("threextalscan_longexposure %s 180", loopT))
}

'

## Temperature Dependent scan: 15K- 90K at 15K temperature interval

def scans_low_to_high_He '
for (loopT=15; loopT < 91; loopT=loopT+15){
eval(sprintf("threextalscan %s 180", loopT))
}
'




---



# sample_alignment_REXS.md


!!! danger "Resonant Elastic X-ray Scattering (REXS)"

Number of elements in the periodic table (K and L edges)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/QM2b%20-%20REXS.png?raw=true){ width="500" }
</figure>

### Beamsplitting polarimeter

The polarization analyzer isolates and measures a unique series of diffraction resonances at the different K-edge.

#### Important SPEC commands for REXS

* For Opening and closing the shutter
a. `opens` - Opening the shutter
b. `closes` - Closing the shutter

* For Pilatus video on and off
a. `pil_von` - Turn pilatus video 'on'
b. `pil_voff` - Turn pilatus video 'off'

* For Position of the displex

a. `wm cryx` - where motor for displex in 'x' directions
b. `wm cryy` - where motor for displex in 'y' directions
c. `wm cryy` - where motor for displex in 'y' directions

* To Get the height correct for the sample 

a. `opens; lup cryz -0.4 0.4 20 0.2; closes` - open the shutter and perform the sample scan in the z directions
b. `umv cryz CEN`- it will go to the center position

* Get the theta correct for the sample 

a. `umv th 10`- Move theta to 10 degrees
b. `opens; lup cryz -0.4 0.4 20 0.2; closes` - open the shutter and perform the sample scan in the z directions

* To Calulate the motor position in a given point in the reciprocal space

a. `setlat` - set lattice paramter information (a, b, c, alpha, beta, gamma) 
b. `pa` - it will show the orientation matrix
c. `ca` 			- calculate motor settings for a given point in reciprocal space
d. `ca 0 0 20` - Calculate the theta, 2theta, chi, and phi for the structural peak (0 0 20)
e. `br` - br and `ubr` - move to the reciprocal space coordinates (HKL)
f. `ubr 0 0 20` - Go to the peak (0 0 20)
g. `or0 0 0 20` - To put the peaks (0 0 20) as first element of the orientation matrix
h. `or1 0 0 18` - To put the peaks (0 0 18) as first element of the orientation matrix

* For moving energy above and below the resonance, perform energyscan 

a. `moveE 11.216` - move the energy for the sample Ir L edge
b. `getE` - Get energy
c. `matchUE 3` -  the undulator 3rd harmonic match with the energy
d. `lscan L-0.1 L+0.1 50 0.5` or `lscan 19.9 20.1 50 0.5` -  Lscan in a range of 0.2, with 50 steps, and 0.5 sec/step
e. `timescan 5` - it is a timescan with 1 datapoint in 5 seconds
f. `opens; EUQscan 11.2 11.24 40 3 3; closes` : Energyscan to get the edge

* For moving the energy to the off-resonance 

a. `moveE 11.23`- Moves to 11.23 keV from current energy
b. `matchUE 3` - the undulator 3rd harmonic match with the energy, the h k l values will be different than the previous one
c. `ubr H K L` - the previous h k l values carried by H K L, we need to do ubr H K L
d. `wh` - where is every position
e. `getE` - it gies current energy information


## If we have two detectors: Pilatus 6 (PIL6) and Pilatus 8 (PIL8). PIL6 is in the beam direction. PIL8 is our sigma-pi channel. The alignment will be based on PIL6. 

## ROI information 

## To set the ROI's for PIL6
a.  `getroi6` -  provide information about the roi chosen in the area detector based on the direction beam position, i.e., xmin, ymin, xsize, ysize.
b. `setroi6 278 67 1 3` - Changing the vertical and horizontal sizes. Examples: 278 and 67 are minimum pixel dimension along x (vertical) and y (horizontal) axis whereas 1 is vertical pixel size (it is minimum) and 3 is horizontal pixel size.

## To set the ROI's for PIL8
a. `getroi` -  provide information about the roi chosen in the area detector based on the direction beam position, i.e., xmin, ymin, xsize, ysize.
b. `setroi 278 67 1 3` - Changing the vertical and horizontal sizes. Examples: 278 and 67 are minimum pixel dimension along x (vertical) and y (horizontal) axis whereas 1 is vertical pixel size (it is minimum) and 3 is horizontal pixel size.

## After setiing up the two peaks, you can set up the macros to optimize the peak positions
def alignfine '
      opens
      lup chi -0.2 0.2 50 0.1
      umv chi CEN
      lup th -0.05 0.05 50 0.1
      umv th CEN
      lup tth -0.1 0.1 50 0.1
      umv tth CEN
      lup th -0.03 0.03 30 0.1
      umv th CEN
      lup tth -0.1 0.1 50 0.1
      umv tth CEN
      lup chi -0.2 0.2 50 0.1
      umv chi CEN
      closes
      wh
‘

## perform the L scan for (0 1 17) peaks 
def getlscan '
      wh
      opens
      lscan 16.96 17.04 120 1
      closes
      moveE 11.20
      matchUE 3
      ubr H K L
      opens
      lscan 16.96 17.04 120 1
      closes
      moveE 11.215
      matchUE 3
‘

## Perform two theta plan
def gettthscan2 ‘
      wh
      alignfine
      opens
      lup cryz -0.2 0.2 40 0.1
      umv cryz CEN
      alignfine
      opens
      th2th -0.04 0.04 80 1
      closes
‘

      



---



# sample_env.md


# Sample environment
If you want to use different sample environment or special equipments, please contact beamline scientist.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/low%20temperature%20capabilitie.png?raw=true){ width="400" }
</figure>


# Users setup at the beamline

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Sample_env.png?raw=true){ width="650" }
</figure>

If you want to run your sample in different environment, please contact us.

Attibutes : Sample type 
Specifications : Powder, Thin-film



---



# temp.md

# Practical guide of the temperature switch between nitrogen and helium

## Consult beamline scientist before changing any temperatures

![sample-cryo1](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sample-cryo1.png?raw=true)

The cryocooler is highly sensitive. To obtain an accurate temperature reading, please adhere to the following instructions. Note that the temperature change occurs gradually, so be patient! It requires time to reach the desired temperature.

![temp-range](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/temp_range.png?raw=true)

## 300K ---> 280K : temperature range

Step 1: Make sure N2 valve is open and helium (He) valve is closed  
Step 2: FOURC > roomT  
(# set temperature to 1st and 2nd controller to 230K and 220K)  
Step 3: Make sure in the controller A (Input A) and C (input C) will to reach the temperature 181K and 220K  
It can be lower if you are going from lower to higher temperature  
Step 4: FOURC > flow_set 6  
(# talk to Staff Scientist for the desired flow rate of your experimental setup)  
Step 5: FOURC > te 300  
(# set the temperature to 300K)

## 200K ---> 270 K : Temperature range

Step 1: Make sure N2 valve is open and helium (He) valve is closed  
Step 2: FOURC > prepN2_high  
(# set temperature to 1st and 2nd controller to 165K and 160K)  
Step 3: Make sure in the controller A (Input A) and C (input C) will to reach the temperature 120K and 160K  
Step 4: FOURC > flow_set 9  
(# talk to Staff Scientist for the desired flow rate of your experimental setup)  
Step 5: FOURC > te 200  
(# set the temperature to 300K)

## 160K ---> 200K : Temperature range

Step 1: Make sure N2 valve is open and helium (He) valve is closed  
Step 2: FOURC > prepN2_medium  
(# set temperature to 1st and 2nd controller to 130K and 110K)  
Step 3: Make sure in the controller A (Input A) and C (input C) will to reach the temperature 101K and 110K  
Step 4: FOURC > flow_set 6  
(# talk to Staff Scientist for the desired flow rate of your experimental setup)  
Step 5: FOURC > te 160  
(# set the temperature to 300K)

## 100K --> 150K : Temperature range

Step 1: Make sure N2 valve is open and helium (He) valve is closed  
Step 2: FOURC > prepN2_low  
(# set temperature to 1st and 2nd controller to 87K and 85K)  
Step 3: Make sure in the controller A (Input A) and C (input C) will to reach the temperature 101K and 110K  
Step 4: FOURC > flow_set 10  
(# talk to Staff Scientist for the desired flow rate of your experimental setup)  
Step 5: FOURC > te 100  
(# set the temperature to 100K)

## Nitrogen to helium switch : Please use Helium sensibly!
110K --> 13K : Cooling temperature of cryocooler with helium (He)

Step 1: FOURC > prepN2_low  
(# set temperature to 1st and 2nd controller to 87K and 85K)  
Step 2: FOURC > te 260  
(# it will setup the temperature in the Lakeshore controller)

If the ice did not melt

Step 3: FOURC > flow_set 6  
Step 4: you need to wait until the temperature of the sample is 260K (it might be lower)  
Step 5: Turn on the He valve and close N2 valve together  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

Step 6: FOURC > runninghelium  
(# it will setup the temperature in the Lakeshore controller)  
Step 7: Wait for base temperature (Input A ~5K Input C ~36K) to stabilize  
Step 8: FOURC > flow_set 10  
Step 9: FOURC > te 14  
(# lowering temperature to 14K or others)  
Step 10: FOURC > spin_xtal_phi  
(# rotate sample 360-->0 and 0-->360 degree in phi directions and you can STOP that by control C)

![Temp-36-4](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Temp%2036-4%201.png?raw=true)

## 13K --> 100K: Heating temperature of cryocooler (change to He to N2 flow)

Step 1: FOURC > prepN2_low  
(# it will setup the temperature setpoints 87K and 85K in the Lakeshore controller Input A and input C)  
Step 2: FOURC > te 240  
(# it will setup the desired sample temperature; here sample temperature is 180 K)  
Step 3: Make sure all the temperature is above 80 K  
a) Input A 87 K  
b) Input B (sample temperature)  
c) Input C 85K in PLD controller  

![Temp-86-83](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Temp%2086-83%201.png?raw=true)

N2 in all conditions should be above 80K  
N2 (channel A, B, C) --> all temperature-->80K  

Step 4: Once Input A, B and C are above 80K, then open the N2 valve and close He valve together  

![N2-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true)

Step 5: FOURC > te 110  
(# increase temperature to 100K or any other desired temperature)

## 300K --> 15K : Room Temperature to base (change N2 to He flow)

Step 1: FOURC > prepN2_low  
(# it will setup the temperature in the Lakeshore controller channel A = 87K and channel B = 85K)  
Step 2: FOURC > Wait until the temperature of the channel A and C is stabilize to 87K and 85K  
Step 3: FOURC > te 260  
(# it will setup the temperature in the Lakeshore controller)  
Step 4: FOURC > flow_set 6  
Step 5: You need to wait until the temperature of the sample is 260K (Make sure you do not have ice)  
Step 6: Turn on the Helium (He) valve and close nitrogen (N2) valve together  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

Step 7: FOURC > runninghelium  
(# it will setup the temperature in the Lakeshore controller)  
Step 8: Wait for base temperature (Input A ~5K Input C ~30K) to stabilize  
Step 9: FOURC > flow_set 10  
Step 10: FOURC > te 15  
(# lowering temperature to 15K or others)  
Step 11: FOURC > spin_xtal_phi  
(# rotate sample 360-->0 and 0-->360 degree in phi directions and you can STOP that by control C)

## 13K --> 300K : Heating temperature of cryocooler (change to He to N2 flow)

Step 1: FOURC > prepN2_low  
(# it will setup the temperature setpoints 230K and 200K in the Lakeshore controller Input A and input C)  
Step 2: FOURC > te 260  
(# it will setup the desired sample temperature; here sample temperature is 240 K)  
Step 3: FOURC > flow_set 6  
Step 4: Make sure all the temperature is above 80 K  
(Input A 87 K, Input B (sample temperature) and Input C 83K in PLD controller)  

N2 in all conditions should be above 80K  
N2 (channel A, B, C) --> all temperature-->80K  

![N2-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true)

Step 5: Turn on the N2 valve and close He valve together  
Step 6: FOURC > roomT  
(# it will setup the temperature setpoints 130K and 110K in the Lakeshore controller Input A and input C and it will to reach the temperature 101K and 110K)  
Step 7: FOURC > te 300  
(# increase temperature to 100K or any other desired temperature)

## 300K --> 500K : Performing experiment above room temperature

We are having problem with high temperature, talk to beamline scientist before doing anything

Step 1: Talk to beamline scientist  
Step 2: Make sure N2 valve is open and He is closed  
Step 3: Physically Turn off compressor (Go to the end of the hutch)  

Press off in the compressor and send a message to the SLACK channel  

![compressor-off](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true)

Step 4: FOURC > te 300  
Step 5: FOURC > turn_off_compressor  
(# increase temperature to 1st and 2nd controller to 300K and 300K)  
Step 6: Make sure in the controller 1 (Input A: 300K and B input C: 300K), it will to reach that temperature and stabilize  
Step 7: FOURC > flow_set 6  
Step 8: FOURC > te 480  
(# increase temperature to 400K)

Note: Above 480K, it took long time to go 498K

## 500K --> 300K (Performing experiment from high temperature to room temperature)

Step 1: Talk to beamline scientist  
Step 2: Make sure N2 valve is open and He is closed  
Step 3: Physically turn on the compressor (Go to the end of the hutch)  

Press on in the compressor and send a message to the SLACK channel  

![compressor-on](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true)

Step 4: FOURC > roomT  
(# increase temperature to 1st and 2nd controller to 130K and 110K)  
Step 5: Make sure in the controller Input A and Input C, it will to reach the temperature 101K and 110K  
Step 6: FOURC > te 300  
(# increase temperature to 300K)

## Turn off the temperature controller

Step 1: Heat the temperature 300K, 300K, 300K  
Step 2: close the compressor  
Step 3: Wait until go to the required temperature  
Step 4: Close the valve

## Problem : Ice formation at low temperature

![icing](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/icing_issue.png?raw=true)

a) Figure 1: Check the distance between the cryo-stream and sample (it should be as close as possible)  
b) Figure 2: Continuously rotate the phi umv phi 360; umv phi 0 at low temperature  
c) Figure 3: Check the gas flow and if needed talk to the staff scientist  

FOURC > flow_set <number>  
FOURC > flow_get

## Problem : High temperature issues

a) Figure 3: Check the gas flow and if needed talk to the staff scientist

## Problem : Accidentally closed the temperature controller

Step 1: Open terminal and type StripTool  
Step 2: Connect to epics PVs  
Step 3: Need to connect to epics PVs that you want to monitor  

LAKESHORE2:KRDG0  
LAKESHORE2:KRDG1  
LAKESHORE2:KRDG2  

Step 4: y-axis click Modify button (same y axis for all the curves)

## Emergency proceduce if the temperature controller fails or Sudden power failure at beamline

Talk to Beamline Scientist or operators --- DONOT TRY THIS WITHOUT ASKING

If the your setup is in nitrogen condition (300K - 80K) and suddenly temperature is dropiing drastically and you don't have controls  

Step 1: Switch the valve Nitrogen to Helium  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

Step 2: Closed the compressor  
Step 3: Change the EPIC PVs range


---

