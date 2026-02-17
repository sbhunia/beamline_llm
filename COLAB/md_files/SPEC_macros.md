# Welcome to SPEC macros
"NOTE": The code is written by [Dr. Jacob Ruff](https://www.chess.cornell.edu/about/staff-directory/jacob-ruff) based on SPEC [certif.com](https://certif.com/).
"spec is internationally recognized as the leading software for instrument control and data acquisition in X-ray diffraction experiments."

# In ID4B, SPEC code is used along with python and C commands. ID4B beamline specific macros are shown below.

## Important SPEC commands for ID4B

* [`userlist.mac`](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/userlist.mac) - Important macos needed for the users, delaied descrispotion are shown below.

* JRs_useful_macros.mac – this is the mac file for beam, motor and slit positions  
* plotlast.mac – this is the mac file for generate??  
* undulator_macro.mac – this is the mac file for undulator stability  
* syncmon.mac – this is the mac file for syncronoze the system  
* fmbo_filter.mac – this is the mac file for filter macros  
* digio.mac – this is the mac file for diti?  
* set_and_get_rois.mac – this is the mac file for set ROI channels  
* multi_pilatus_v5.mac – this is the mac file for detector  
* Lakeshore336cryocool.mac – this is the mac file for temperature macros  
* energy_pv.mac – this is the mac file for energy macros  
* undulator_2A.mac – this is the mac file for undulator stablibility macros
    
## Detailed description of macros

The codes are in github repository [JRs_useful_macros.mac](https://github.com/suchismitasarker/CLASSE-id4b/blob/main/JRs_useful_macros.mac)

1.  Define a macro vbeamscan based on passing four arrguments start, finish, interval and time parameter scans
2.  Define a macro newbeam based on passing four arrguments start, finish, interval and time parameter scans
3.  Define a macro hbeamscan based on passing four arrguments start, finish, interval and time parameter scans
4.  Define a macro monocromator position by "def wmono 'wm monu mond monoff montrav mond_x monzu monzd monxu monxd' "
5.  Define a macro for mirror posiiton by " def wmirror 'wm mird miru mirbd mirbu' "
6.  Define a macro for optical table
7.  Define a macro for slit position
8.  Define a macro for tweakup the monochromator d position wby scanning both mond and undulator motors
9.  Define where is 6M detectors
10. Define how to park the 6M detector




