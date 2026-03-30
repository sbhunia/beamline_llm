# Practical guide of the temperature switch between nitrogen and helium

## Consult beamline scientist before changing any temperatures

![sample-cryo1](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/sample-cryo1.png?raw=true)

The cryocooler is highly sensitive. To obtain an accurate temperature reading, please adhere to the following instructions. Note that the temperature change occurs gradually, so be patient! It requires time to reach the desired temperature.

![temp-range](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/temp_range.png?raw=true)

---

## Change of temperature from 300K to 280K between nitrogen and helium

* Step 1: Make sure N2 valve is open and helium (He) valve is closed  
* Step 2: `FOURC > roomT`  
  (# set temperature to 1st and 2nd controller to 230K and 220K)  
* Step 3: Make sure controller A (Input A) and C (Input C) reach 181K and 220K  
* Step 4: `FOURC > flow_set 6`  
  (# talk to Staff Scientist for desired flow rate)  
* Step 5: `FOURC > te 300`

---

## Change of temperature from 200K to 270K between nitrogen and helium

* Step 1: Make sure N2 valve is open and helium (He) valve is closed  
* Step 2: `FOURC > prepN2_high`  
  (# set controller to 165K and 160K)  
* Step 3: Ensure Input A and C reach 120K and 160K  
* Step 4: `FOURC > flow_set 9`  
* Step 5: `FOURC > te 200`

---

## Change of temperature from 160K to 200K between nitrogen and helium

* Step 1: Make sure N2 valve is open and helium (He) valve is closed  
* Step 2: `FOURC > prepN2_medium`  
  (# set controller to 130K and 110K)  
* Step 3: Ensure Input A and C reach 101K and 110K  
* Step 4: `FOURC > flow_set 6`  
* Step 5: `FOURC > te 160`

---

## Change of temperature from 100K to 150K between nitrogen and helium

* Step 1: Make sure N2 valve is open and helium (He) valve is closed  
* Step 2: `FOURC > prepN2_low`  
  (# set controller to 87K and 85K)  
* Step 3: Ensure Input A and C reach 101K and 110K  
* Step 4: `FOURC > flow_set 10`  
* Step 5: `FOURC > te 100`

---

## Change of temperature from 110K to 13K between nitrogen and helium

* Step 1: `FOURC > prepN2_low`  
* Step 2: `FOURC > te 260`

If ice did not melt:

* Step 3: `FOURC > flow_set 6`  
* Step 4: Wait until sample reaches ~260K  
* Step 5: Turn ON He valve and close N2 valve  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

* Step 6: `FOURC > runninghelium`  
* Step 7: Wait for stabilization (A ~5K, C ~36K)  
* Step 8: `FOURC > flow_set 10`  
* Step 9: `FOURC > te 14`  
* Step 10: `FOURC > spin_xtal_phi`

---

## Change of temperature from 13K to 100K between nitrogen and helium (He and N2)

* Step 1: `FOURC > prepN2_low`  
* Step 2: `FOURC > te 240`  
* Step 3: Ensure all temperatures > 80K  
* Step 4: Open N2 valve and close He valve  
* Step 5: `FOURC > te 110`
![N2-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true)



---

## Change of temperature from 300K to 15K (Room → Base)

* Step 1: `FOURC > prepN2_low`  
* Step 2: Wait until A & C stabilize (87K, 85K)  
* Step 3: `FOURC > te 260`  
* Step 4: `FOURC > flow_set 6`  
* Step 5: Wait until sample reaches 260K  
* Step 6: Switch N2 → He  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

* Step 7: `FOURC > runninghelium`  
* Step 8: Wait for base temp  
* Step 9: `FOURC > flow_set 10`  
* Step 10: `FOURC > te 15`  
* Step 11: `FOURC > spin_xtal_phi`

---

## Change of temperature from 13K to 300K (He → N2)

* Step 1: `FOURC > prepN2_low`  
* Step 2: `FOURC > te 260`  
* Step 3: `FOURC > flow_set 6`  
* Step 4: Ensure all temps > 80K  

![N2-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/N2%20open2.png?raw=true)

* Step 5: Switch He → N2  
* Step 6: `FOURC > roomT`  
* Step 7: `FOURC > te 300`

---

## Change of temperature from 300K to 500K between nitrogen and helium

* Step 1: Talk to beamline scientist  
* Step 2: Ensure N2 open, He closed  
* Step 3: Turn OFF compressor  

![compressor-off](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true)

* Step 4: `FOURC > te 300`  
* Step 5: `FOURC > turn_off_compressor`  
* Step 6: Wait until stable  
* Step 7: `FOURC > flow_set 6`  
* Step 8: `FOURC > te 480`

---

## Change of temperature from 500K to 300K between nitrogen and helium

* Step 1: Talk to beamline scientist  
* Step 2: Ensure N2 open, He closed  
* Step 3: Turn ON compressor  

![compressor-on](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/compressor.jpeg?raw=true)

* Step 4: `FOURC > roomT`  
* Step 5: Wait for stabilization  
* Step 6: `FOURC > te 300`

---

## Turn off temperature controller

* Step 1: Heat to 300K  
* Step 2: Close compressor  
* Step 3: Wait until stable  
* Step 4: Close valve

---

## Problem: Ice formation

## Steps to follow when there is Ice Formation in cryocooler
![icing](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/icing_issue.png?raw=true)

* Step 1: Check cryo-stream distance  
* Step 2: Rotate phi continuously  
* Step 3: Check gas flow  

Commands:
`FOURC > flow_set <number>`  
`FOURC > flow_get`

---

## Problem: High temperature issues

## Steps to follow when there is a high temperature issue in Cryocooler
* Step 1: Check gas flow  
* Step 2: Talk to staff scientist

---

## Problem: Controller accidentally closed
## STEPS to follow when Controller has been accidentally closed
* Step 1: Open terminal → `StripTool`  
* Step 2: Connect to EPICS PVs  
* Step 3: Add:
  - `LAKESHORE2:KRDG0`  
  - `LAKESHORE2:KRDG1`  
  - `LAKESHORE2:KRDG2`  
* Step 4: Modify y-axis

---

## Emergency procedure involved in temperature switch between Helium and Nitrogen

* Step 1: Talk to beamline scientist  
* Step 2: Switch N2 → He  

![He-open](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/He%20open%203.png?raw=true)

* Step 3: Close compressor  
* Step 4: Adjust EPICS PV range