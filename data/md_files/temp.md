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
