

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


