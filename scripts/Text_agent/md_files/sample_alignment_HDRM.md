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


