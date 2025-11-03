NOTES 2/27/21:

The file multi_pilatus_v5_p6m.mac incorporates a new global variable, PIL_BASE_PATH, 
that permits setting "/ramdisk" as the base of the target directory for images. As with prior practice, the macros still check that the SPEC CWD is on /nfs/chess/daq/../STATION_ID/. 

Maybe we also need a flag to turn off checks that the target directory exists. In that case, the p6m branch should be able to be merged back into master without breaking anything.

 
