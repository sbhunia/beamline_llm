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
