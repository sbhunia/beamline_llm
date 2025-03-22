
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

#### STEP 1: If you lost fourc/SPEC terminal 
* Open terminal 
* type `findspec` (it will provide all the spec information)
* Check the getPid number
* type `fg <getPid number>` (example # fg 21192) 

##### STEP 2: Talk to beamline scientist 

If you doesn't find anythng after STEP 1 fourc/SPEC terminal 
* If you not find the SPEC terminal, then type below command
* `kill -9 <getPid number>` (example# kill -9 21192)
* Open a new terminal 
* Type ‘fourc’

###### If you fourc/SPEC doesn't work 
* Open terminal 
* type `quit`
* type `fourc`


##### If SPEC window is lost

* Open an terminal 
* type `findspec`
* If it is hidding, then type `fg <PID number>`


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
     


