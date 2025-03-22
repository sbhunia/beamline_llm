

# Practical guide of the temperature switch between nitrogen and helium

#### Consult beamline scientist before changing any temperatures


<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sample-cryo1.png?raw=true){ width="500" }
</figure>

###### The cryocooler is highly sensitive. To obtain an accurate temperature reading, please adhere to the following instructions. Note that the temperature change occurs gradually, so be patient! It requires time to reach the desired temperature.

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/temp_range.png?raw=true){ width="800" }
</figure>




<b><i><u> 280K ---> 300K : temperature range </b></u>

* Step 1 : Make sure N2 valve is open and helium (He) valve is closed
* Step 2: <i> FOURC > `roomT`  (# set temperature to 1st and 2nd controller to 230K and 220K)
* Step 3 : Make sure in the controller A (Input A) and C (input C) will to reach the temperature <b>181K </b> and <b>220K </b>.
* Step 4: <i> FOURC > `flow_set 6` ( # talk to Staff Scientist for the desired flow rate of your experimental setup)
* Step 5 : FOURC > `te 300` </i>   (# set the temperature to 300K)


<b><i><u> 200K ---> 270 K : Temperature range </b></u>

* Step 1 : Make sure N2 valve is open and helium (He) valve is closed
* Step 2: <i> FOURC > `prepN2_high`  (# set temperature to 1st and 2nd controller to 165K and 160K)
* Step 3 : Make sure in the controller A (Input A) and C (input C) will to reach the temperature <b>120K </b> and <b>160K </b>.
* Step 4: <i> FOURC > `flow_set 9` ( # talk to Staff Scientist for the desired flow rate of your experimental setup)
* Step 5 : FOURC > `te 200` </i>   (# set the temperature to 300K)


<b><i><u> 160K ---> 200K : Temperature range </b></u>

* Step 1 : Make sure N2 valve is open and helium (He) valve is closed
* Step 2: <i> FOURC > `prepN2_medium`  (# set temperature to 1st and 2nd controller to 130K and 110K)
* Step 3 : Make sure in the controller A (Input A) and C (input C) will to reach the temperature <b>101K </b> and <b>110K </b>.
* Step 4: <i> FOURC > `flow_set 6` ( # talk to Staff Scientist for the desired flow rate of your experimental setup)
* Step 5 : FOURC > `te 160` </i>   (# set the temperature to 300K)

<b><i><u> 100K --> 150K : Temperature range </b></u>

* Step 1 : Make sure N2 valve is open and helium (He) valve is closed
* Step 2: <i> FOURC > `prepN2_low`  (# set temperature to 1st and 2nd controller to 87K and 85K)
* Step 3 : Make sure in the controller A (Input A) and C (input C) will to reach the temperature <b>101K </b> and <b>110K </b>.
* Step 4: <i> FOURC > `flow_set 10` ( # talk to Staff Scientist for the desired flow rate of your experimental setup)
* Step 5 : FOURC > `te 100` </i>   (# set the temperature to 100K)


!!! danger "Nitrogen to helium switch : Please use Helium sensibly!"
<b><i><u> 110K --> 13K : Cooling temperature of cryocooler with helium (He) </b></u> 

* Step 1: <i> FOURC > `prepN2_low`  (# set temperature to 1st and 2nd controller to 87K and 85K)
* Step 2 : <i> FOURC > `te 260` </i> (# it will setup the temperature in the Lakeshore controller)
If the ice did not melt 
* Step 3 : <i> FOURC > `flow_set 6` </i>
* Step 4: <i> you need to wait until the temperature of the sample is 260K (it might be lower)
* Step 5 : Turn on the He valve  and close N2 valve together

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true){ width="500" }
</figure>

* Step 6 : <i> FOURC > `runninghelium` </i> (# it will setup the temperature in the Lakeshore controller)
* Step 7 : Wait for base temperature (Input A ~5K Input C ~36K) to stabilize (look at the plot below)
* Step 8 : <i> FOURC > `flow_set 10` </i>
* Step 9 : <i> FOURC > `te 14` </i>   (# lowering temperature to 14K or others)
* Step 10: <i> FOURC > `spin_xtal_phi` </i> (# rotate sample 360-->0 and 0-->360 degree in phi directions and you can STOP that by control C )

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Temp%2036-4%201.png?raw=true){ width="700" }
</figure>


<b><i><u>  13K --> 100K: Heating temperature of cryocooler (change to He to N<sub>2</sub> flow)</b></u>


* Step 1 : <i> FOURC > `prepN2_low` </i> (# it will setup the temperature setpoints 87K and 85K in the Lakeshore controller Input A and input C)
* Step 2 : <i> FOURC > `te 240` </i> (# it will setup the desired sample temperature; here sample temperature is 180 K)
* Step 3 : <b> Make sure all the temperature is above 80 K (Input A 87 K, Input B (sample temperature) and Input C 85K in PLD controller) </b>

  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Temp%2086-83%201.png?raw=true){ width="600" }
</figure>

!!! danger
    </i>N<sub>2</sub> in all conditions should be above 80K (N<sub>2</sub> (channel A, B, C) --> all temperature-->80K)
<figure markdown>
* Step 4 : <b> Once Input A, B and C are above 80K, then open the N2 valve and close He valve together </b>

  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true){ width="600" }
</figure>

* Step 5 : <i> FOURC > `te 110` </i>   (# increase temperature to 100K or any other desired temperature)


<b><i><u>  300K --> 15K : Room Temperature to base (change N<sub>2</sub> to He flow)</b></u>

* Step 1 : <i> FOURC > `prepN2_low` </i> (# it will setup the temperature in the Lakeshore controller channel A = 87K and channel B = 85K)
* Step 2 : <i> FOURC > Wait until the temperature of the channel A and C is stabilize to 87K and 85K
* Step 3 : <i> FOURC > `te 260` </i> (# it will setup the temperature in the Lakeshore controller)
* Step 4 : <i> FOURC > `flow_set 6` </i>
* Step 5: <i> You need to wait until the temperature of the sample is 260K (Make sure you do not have ice)
* Step 6 : Turn on the Helium (He) valve  and close nitrogen (N2) valve together

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true){ width="500" }
</figure>

* Step 7 : <i> FOURC > `runninghelium` </i> (# it will setup the temperature in the Lakeshore controller)
* Step 8 : Wait for base temperature (Input A ~5K Input C ~30K) to stabilize (look at the plot above)
* Step 8 : <i> FOURC > `flow_set 10` </i>
* Step 9 : <i> FOURC > `te 15` </i>   (# lowering temperature to 15K or others)
* Step 10: <i> FOURC > `spin_xtal_phi` </i> (# rotate sample 360-->0 and 0-->360 degree in phi directions and you can STOP that by control C )


<b><i><u> 13K --> 300K : Heating temperature of cryocooler  (change to He to N<sub>2</sub> flow)</b></u>


* Step 1 : <i> FOURC > `prepN2_low` </i> (# it will setup the temperature setpoints 230K and 200K in the Lakeshore controller Input A and input C)
* Step 2 : <i> FOURC > `te 260` </i> (# it will setup the desired sample temperature; here sample temperature is 240 K)
* Step 3: <i> FOURC > `flow_set 6` </i> 
* Step 4 : <b> Make sure all the temperature is above 80 K (Input A 87 K, Input B (sample temperature) and Input C 83K in PLD controller) </b>
!!! danger
    </i>N<sub>2</sub> in all conditions should be above 80K (N<sub>2</sub> (channel A, B, C) --> all temperature-->80K)
<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true){ width="600" }
</figure>

* Step 5 : Turn on the N2 valve  and close He valve together
* Step 6 : <i> FOURC > `roomT` </i>   (# it will setup the temperature setpoints 130K and 110K in the Lakeshore controller Input A and input C and it will to reach the temperature 101K and 110K.)
* Step 7 : <i> FOURC > `te 300` </i>   (# increase temperature to 100K or any other desired temperature)



<b><i><u>  300K --> 500K : Performing experiment above room temperature </b></u>

!!! danger
    We are having problem with high temperature, talk to beamline scientist before doing anything
* Step 1 : <b>Talk to beamline scientist </b>
* Step 2 : Make sure N2 valve is open and He is closed
* Step 3 : Physically `Turn off` compressor (Go to the end of the hutch)

  * press `off` in the compressor (see the image below)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true){ width="300" }
</figure>

* Step 4 : <i> FOURC > `te 300`
* Step 5: <i> FOURC > `turn_off_compressor`  (# increase temperature to 1st and 2nd controller to 300K and 300K)
* Step 5: Make sure in the controller 1 (Input A: 300K and B input C: 300K), it will to reach that temperature and stabilize.
* Step 6 : <i> FOURC > `flow_set 6`
* Step 7 : FOURC > `te 480` </i>   (# increase temperature to 400K)

 <i> Note: Above 480K, it took long time to go 498K </i> 

<b><i><u>  500K --> 300K (Performing experiment from high temperature to room temperature )</b></u>

* Step 1 : <b>Talk to beamline scientist </b>
* Step 1 : Make sure N2 valve is open and He is closed
* Step 2 : Physically `turn on` the compressor (Go to the end of the hutch)

  * press `on` in the compressor (see the image below)

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true){ width="300" }
</figure>

* Step 3: <i> FOURC > `roomT`  (# increase temperature to 1st and 2nd controller to 130K and 110K)
* Step 3 : Make sure in the controller  Input A and Input C, it will to reach the temperature 101K and 110K.
* Step 4 : FOURC > `te 300` </i>   (# increase temperature to 300K)


<b><i><u> Turn off the temperature controller </b></i></u>

* Step 1 : Heat the temperature 300K, 300K, 300K 
* Step 2 : close the compressor
* Step 3 : Wait until go to the required temperature
* Step 4 : Close the valve



# Problem : Ice formation at low temperature

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/icing_issue.png?raw=true){ width="600" }
</figure>
 
* <i><b> a) Figure 1</b></i> : Check the distance between the cryo-stream and sample (it should be as close as possible)
* <i><b> b) Figure 2</b></i> : Continuously rotate the phi `umv phi 360; umv phi 0` at low temperature
* <i><b> c) Figure 3</b></i> : Check the gas flow and if needed talk to the staff scientist 
        
    * `FOURC> flow_set <number>`
    * `FOURC> flow_get `


# Problem : High temperature issues
* <i><b> a) Figure 3</b></i> : Check the gas flow and if needed talk to the staff scientist

# Problem : Accidentally closed the temperature controller

* <i><b> Step 1 </b></i> : Open terminal and type ` StripTool`
* <i><b> Step 2 </b></i> : Connect to epics PVs


* Need to connect to epics PVs that you want to monitor

      * LAKESHORE2:KRDG0
      * LAKESHORE2:KRDG1
      * LAKESHORE2:KRDG2

* y-axis click “Modify” button (same y axis for all the curves)


#### Emergency proceduce if the temperature controller fails or Sudden power failure at beamline

!!! danger "Talk to Beamline Scientist or operators --- DONOT TRY THIS WITHOUT ASKING" 

* If the your setup is in nitrogen condition (300K - 80K) and suddenly temperature is dropiing drastically and you don't have controls 
  * Switch the valve Nitrogen to Helium 

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true){ width="500" }
</figure>

  * Closed the compressor

  * Change the EPIC PVs range


