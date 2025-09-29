## Cryocoolers



<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-photos/blob/main/Crysocooler.png?raw=true)

</figure>

The cryocooler is manufactured by [CYRO Industries of America, Inc.](http://www.cryoindustries.com/).

<i> Close-circle cryostats are installed in &#60QM&#62<sup>2</sup> allowing samples to be comprehensively studied in a wide range of temperatures from 12K to 500K. The cryocooler can operate both helium (12K to 300K) and nitrogen gas (300K to 500K ) using a single stream flow. In-house nitrogen and helium gas are used for cryocoolers. Just by switching the knob outside of the hutch, the gas supply can be altered. 

The external tip-heater prevents frost and maintains a dry tip that helps to create an ice-free sample environment at low temperatures. A platinum temperature sensor is installed to control the low alarm setting temperature that triggers back the temperature controller to energize and maintain the ice-free environment. 

The main component of the cryostat can be divided into five different components: 
<br>

* (i) <b> source </b> : the refrigerator or the cryostat act as a source to cool a reliable cryogenic temperature for a long continuous periods
<br>

* (ii)<b> compressor </b>
<br>

* (iii) <b> PID temperature controller </b>: Cryogenic temperature controlled Model 336 manufactured by Lake Shore is used.  The controller’s zone tuning feature allows you to measure and control temperatures seamlessly from 300 mK to over 1,500 K by automatically switching temperature sensor inputs [1].
<br>

* (iv) <b> Power supply </b> : 30 V digital and 24V DC are used
<br> 

* (v) <b> Gas flow controller </b> : The digital flow automatically control and displays the flow rate

<b> Gas flow parameters </b>
<br>
<b> Helium gas</b>: Normal flow rate is between 8 – 12 liters/min, typically 11 l/min
</br>
<b> Nitrogen gas </b> : Normal flow rate is between 8 – 12 liters/min, typically 9 l/min.
</br>

<b> Safety </b>

* Do not touch the cold helium and nitrogen gas stream. Exposure to the skin of the cold gas could result in severe injuries.
* The dewar system has pressure relief protection installed. Do not remove pressure reliefs or check valves.

Motors

| Motor | Commands | Comments | 
| -------------- | :---------: | ---------- | 
| Temperature controller | sampleT | Set the temperature |  


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
