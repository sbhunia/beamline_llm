# SPEC- ID4B


## Welcome to ID4B SPEC command

!!! hint "SPEC Detailed Descriptions"
    For full documentation visit [certif.com](https://certif.com/).
    In ID4B, we used several SPEC along with python and C written by [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff).


"spec is internationally recognized as the leading software for instrument control and data acquisition in X-ray diffraction experiments."

---
Few important commands are shown below.

---
!!! danger " SPEC Commands for ID4B" 
    More detaiils can be found in [SPEC manual](https://certif.com/) and ID4B-SPEC Examples.

## Important SPEC commands 

* `mkdir` - Create a new directotry.
* `a2scan` - two-motor scan.
* `abscan` - incident-reflected angle scan.
* `br` - br and ubr - move to the reciprocal space coordinates (HKL).
* `ca` 			- calculate motor settings for a given point in reciprocal space
* `cal` 			- calculate motor settings for a given point in reciprocal space
* `cat` 			- UNIX shell cat command
* `cd` 			- change working directory
* `cmAX` 		- Compumotor AX motor controller
* `config` 		- edit the hardware configuration
* `config_adm` 		- configuration - administer hardware configuration file
* `constant` 		- define a constant global symbol
* `counting` 		- timer/scaler commands, macros and variables
* `cscan` 		- Continuous Scans
* `ct` 			- count and print results
* `dscan/lup` 		- motor scan relative to the starting position
* `d2scan` 		- two-motor scan relative to the starting positions
* `def` 			- def and rdef - define a macro
* `disable` 		- disable and enable - Disable and Enable Hardware
* `do` 			- execute a command file
* `dtscan` 		- relative temperature scan
* `dxp` 			- XIA DXP CAMAC MCA
* `encode` 		- encode()/decode() - data stream manipulation
* `epics` 		- EPICS specific functions
* `files` 		- conventions for file/device output
* `flow` 		- flow control
* `flyscan` 		- Continuous Scans with Multichannel Scalers
* `fourc` 		- 4-circle geometry modes
* `funcs` 		- functions - built-in functions
* `global` 		- declare global variables
* `getE`        - get the energy
* `getroi`      - get the region of interest
* `hbeamscan`   - Horizontal direction beam scan based on start, finish, interval and time arrguments
* `history` 		- command recall facility
* `hklscan` 		- general linear scan in reciprocal space
* `hscan` 		- scan along the H-axis in reciprocal space
* `install` 		- spec installation procedure
* `l` 			- UNIX file listing
* `libedit` 		- libedit/readline - command line recall and editing
* `lm` 			- list motor software limits
* `ls` 			- UNIX file listing
* `lscan` 		- scan along the L-axis in reciprocal space
* `lup chi`     - motor 'chi' scan relative to the starting position
* `lup th`      - motor 'th' scan relative to the starting position
* `lup tth`     - motor 'two theta' scan relative to the starting position
* `lup phi`     - motor 'phi' scan relative to the starting position
* `macros` 		- description of macro facility
* `matchUE` 		- match undulator energy
* `maxk`        - maximum position at k reciprocal space
* `wm monchi`      - where is monochromator  chi  
* `mk / umk` 		- move to the reciprocal space coordinates (HKL)
* `mono` 		- monochromator - monochromator control macros
* `motors` 		- commands and functions for controlling motors
* `move_info` 		- move_info() - returns what would happen on a move
* `moveE`       - move the energy 
* `mr` 			- move to a given angle of specular reflection
* `mv` 			- mv and umv - move one motor
* `mvd` 			- move a motor in dial units
* `mvr` 			- mvr and umvr - move a single motor relative to its current position
* `umv th CEN`      - move theta motor to center
* `mond`            - monocromator d posiiron
* `montrav`         - monochromator in trnasverse direction
* `newvbeam`        - new beam position based on vertical beam or horizontal beam scan
* `newfile` 		- data file management
* `newmac` 		- re-read the standard macro definitions
* `nu`          - `???????`
* `or0`         - 
* `or1`         - 
* `or_swap`     - 
* `os1`         - optical slit 1 position to 0
* `os2`         - optical slit 1 position to 0
* `pwd` 		- print spec's current working directory
* `pa`          - 
* `park6m`      - park the 6M PILATUS detector to 175m (x), 924.5m (y) and 200m (z) in  directions
* `pil_von`     - PILATUS video on  
* `pil_voff`    - PILATUS video off
* `pil_setdir`  - PILATUS set directory
* `pil_setup PIL6`  - PILATUS setup 
* `pil_settrig "Internal"`  -
* `pil_unsetup 0`   - PILATUS unset 
* `pl_xMAX`     - show the maximum value of the plot in x-direction
* `plotselect pilroi`   - plot select PILATUS ROI
* `qdo` 		- execute a command file without echo
* `quickfly`    -
* `quick_collect`   -  
* `rscan` 		- specular reflectivity scan
* `r2scan` 		- reflectivity background scans
* `readline` 		- libedit/readline - command line recall and editing
* `resume` 		- continue an aborted scan
* `roi` 		- region of Interest counters
* `samz`        - moving sample z direction
* `scans` 		- scans and scans.4 - read data from ASCII spec data format scan files
* `server` 		- spec server/client - issue commands and control hardware remotely
* `set` 		- define the user angle of a motor
* `setfilter`   - set filter
* `set_dial` 		- define the dial position of a motor
* `setlat`      - set lattice
* `set_lm` 		- set lower and upper software limits
* `set_sim` 		- set simulate (no hardware) mode
* `setplot` 		- set plotting options
* `setpowder` 		- configure powder-averaged scans
* `setscans` 		- configure scan options
* `showtemp` 		- display the current temperature
* `sharpopt`        - 
* `sixc` 		- 6-circle geometry modes
* `spec` 		- spec, fourc, twoc, surf, etc. - X-ray diffractometer operation for specific configurations
* `spec_menu` 		- spec_menu() - create interactive menu from specifications
* `spec_par` 		- spec_par() - sets internal parameters
* `splot`       - plot the plotselect of specific values
* `syncE`       - synchronize E
* `tw tabzd tabzui tabzuo` -    tewak table 
* `te` 			- read or set the temperature
* `teramp` 		- ramp the temperature to a new set point
* `tscan` 		- temperature scan
* `th2th`       - theta two theta scan
* `tw` 			- "tweak" motors
* `tweakup` 	- scan the monochromator in d direction (mond), go to the midlle and scan the undulator and move to the highest position
* `unkludgenu`  - `??????`
* `vi` 			- invokes the standard UNIX visual editor
* `vscan` 		- Variable Step Size Scans
* `vbeamscan` 	- Vertical direction beam scan based on start, finish, interval and time arrguments
* `w` 			- wait for moving and counting and then beep
* `wa` 			- list all motor positions
* `wait` 		- wait() - synchronization with moving, counting and other activity
* `wfilter`     - where is filters
* `wideopt`     - 
* `diftabx`     - diffractometer movement in x directions
* `diftabz`     - diffractometer movement in z directions
* `wh` 			- where, principal axes and reciprocal space
* `whats` 		- identify what an object is
* `wm` 			- print information about one or more motors
* `wmono`       - where is monochromatic beam
* `wmonoall`    - where motor and their position including the motors, phi and filters 
* `wmonoall`    - where is mirror position
* `wot`         - where is optical tables
* `ws1`         - where is first slit
* `ws2`         - where is second slit
* `w6m`         - where is 6M detector
* `wslits`      - where is both slit 1 and slit 2

---

<b><i> If you encounter any new commands during your sample run, please <a href = "mailto: ss3428@cornell.edu">send an email </a> and we will add that to the list <i><b>.