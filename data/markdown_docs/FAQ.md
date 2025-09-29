

## Frequesnly ask questions (FAQ)
!!! hint "Frequesnly ask questions (FAQ)"
    Answers are given by [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) and Suchismita Sarker



###### Q. How is the measurement time and what is the angle step size when rotating the single crystal?

<i> These parameters are adjustable, of course, but the most “typical” choice is continuous rotation, 0.1 degree angular integrations, collecting 2 or 3 redundant 360 degree rotations with different rotation axes, and ~0.1 seconds per frame.  So, full data collection is ~3600 frames x 3 scans x 0.1 seconds = 18 minutes of data collection at a single temperature.  There is motor movement overhead that adds time to to this, but basically collecting one comprehensive dataset at one temperature in <30 minutes is reasonable </i>. 


###### Q. What is the photon energy and Qmax for 3D-PDF experiment?

<i> Presently QM2 has a maximum operating energy of 52 keV. The minimum sample-to-detector distance with the Pilatus6M is ~380mm. This would give you a two-theta max < 45 degrees, and a QMax <~ 20 inv A, depending on how you center the detector on the beam </i>.

###### Q. What is the temperature range available for 3D-dPDF? We are requesting cryostream-like temperature region (100~500 K), but it would be intesting to know if any lower or higher tempearture setup accessible.

<i> Our gas cryocooler system gives the best quality data, since there are no windows. Our system operates using either helium or nitrogen, and can switch on the fly. With helium, it operates from ~13K to 180K, and with nitrogen from ~95K to 500K. When using this system, we recommend users mount samples using crystallography loops, as noted above </i>.


##### Q. 2. What is the suitable single crystal size in volume and dimension lengths so that it can be covered by the beam when rotating (not too large or too small)?

<i> The beam at 4B is ~200 microns tall and ~1mm wide.  Typically, we mount crystals using mitigen crystallography loops if using a gas cryocooler, or on copper posts if using a closed cycle cryostat.  The ideal crystal size/shape depends a little on the mounting method. Generally, though, you want to keep the scattering volume constant while rotating, and you want to have crystals <~ one attenuation length in at least 2 dimensions. Samples can in principle be longer along the rotation axis direction - like a cylinder or bar where the short directions are ~ 100 microns but the long direction is several mm, still works well </i>. 

###### Q: Where is my data?
<i>The data stored at id4b, after processing the data your can find that in id4baux. </i>

###### Q: How to transfer the data?
<i> You should use globus to transfer your data.</i>


##### Q. How to recover if the computer fail?
<i> Talk to the beamline scientist </i>


##### Q. Can I run thin-film samples at the beamline? What is the minimum thickness of the sample that can be examind?
<i> Yes, thin-film samples can be successfully run at the beamline. The thinnest sample examined so far has had a thickness of 3 nm. </i>







