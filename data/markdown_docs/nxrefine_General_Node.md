


# NXRefine
The code is written by Dr. Ray Osborn. More details will be available [NXRefine](https://nexpy.github.io/nxrefine/).The code provides various tools for stacking the raw data, finding Bragg peaks, solving the orientation matrix, and finally providing the HKL. 


# Data Policy 
!!! hint "Data policy"
      We only stored the raw data for six months and processed data for a year. Please process the data and copy it to your server. If you need more time, then consult your beamline scientist.



# NXRefine General Nodes

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/Beamline%20computers.png?raw=true)
</figure>


===============================================================================

* (i) <b> Step 1 :

<i> Make sure you have permission for the desired folders,  before running the job in the queue, ask your beamline scientist to change the permission of the folder (it is always need to be updated). Also, make sure you have the <i> parent file </i> for each folders, otherwise the code will not work. </b> </i>

!!! danger "Change the < classe_id > to your own CLASSE ID" 

* (ii) <b> Step 2 :</b> Login to lnx201

        ssh <classe_id>@lnx201.classe.cornell.edu


* (iii) <b> Step 3 :</b> 
        
        qrsh -q interactive.q -l mem_free=350G -pe sge_pe 20



* (vi) <b> Step 4 :</b>: Go to the desired data analayis forder (it will your folder in aux)

        cd /nfs/chess/id4baux/2024-1/<BTR-3946-a>/


* (vi) <b> Step 5 :</b>: 
Changed the desired steps for nxrefine from the folder or if you know how to use vim, then do to change the qsub file and do that necessasy steps 

* Make sure you have change the file path and the threshold of the nxfind of the sample

* If you are nomachine, you can change the qsub_jobs_****.sh file directly based on the steps you want to perform in the data processing  

        vim qsub_jobs_<name of the user>.sh 


* (vii) <b> Step 6 : </b> Run the job in lnx201 (make sure path is correct)

        qsub -q all.q -l mem_free=350G -pe sge_pe 32 /nfs/chess/id4baux/2025-1/sarker-3946-a/qsub_jobs_<name of the file>.sh

!!! danger "If it did not work, try to use less memory and submit the job again" 
* You can change mem_free = 200, below is the example
        
        qsub -q all.q -l mem_free=200G -pe sge_pe 32 /nfs/chess/id4baux/2025-1/sarker-3946-a/qsub_jobs_<name of the file>.sh



* (viii) <b> Step 9 :</b> Check the status

        qstat


* (ix) <b> Step 10 :</b> See the status ebaborately


        cat qsub_jobs_<classe_id>.sh.e7231424

* (x) <b> Step 11 :</b> Finally after you the data procesing

        chmod -R 777 /nfs/chess/id4baux/2025-1/<project_name>

        Example: 

        chmod -R 777 /nfs/chess/id4baux/2025-1/sarker-3490-a

## Want to reprocess the data with higher step size or better resolution?
 
!!! hint "Reprocessing steps"

    Once you have received the HKLI data from the QM2 beamline, you can visualize the data. If you want higher resolution in nxrefine trnasform stage and nxcombine you can modify that. Below is the help command to see what paramters you can change in `nxtransform` and `nxcombine` stage.


        nxtransform --h
        usage: nxtransform [-h] -d DIRECTORY [-e ENTRIES [ENTRIES ...]] [-qh QH QH QH] [-qk QK QK QK] [-ql QL QL QL] [-R] [-M] [-o] [-q]
        Perform CCTW transform options:
        -h, --help show this help message and exit
        -d DIRECTORY, --directory DIRECTORY scan directory
        -e ENTRIES [ENTRIES ...], --entries ENTRIES [ENTRIES ...] names of entries to be processed
        -qh QH QH QH Qh - min, step, max
        -qk QK QK QK Qk - min, step, max
        -ql QL QL QL Ql - min, step, max
        -R, --regular perform regular transform
        -M, --mask perform transform with 3D mask
        -o, --overwrite overwrite existing transforms
        -q, --queue add to server task queue


        nxcombine --h
        usage: nxcombine [-h] [-d DIRECTORY] [-e ENTRIES [ENTRIES ...]] [-R] [-M] [-o] [-q]

        Combine CCTW transforms

        options:
        -h, --help            show this help message and exit
        -d DIRECTORY, --directory DIRECTORY
                                scan directory
        -e ENTRIES [ENTRIES ...], --entries ENTRIES [ENTRIES ...]
                                names of entries to be combined.
        -R, --regular         combine transforms
        -M, --mask            combine transforms with 3D mask
        -o, --overwrite       overwrite existing transform
        -q, --queue           add to server task queue

Now based on the `help` command, you can modify the script and add the `min` `stepsize` `max` for your desired data. For example, previously your HKLI and step size is below

<figure markdown>
  ![Image title](https://github.com/suchismitasarker/CHESS-ID4B-QM2/blob/main/pictures/transform.png?raw=true){ width="450"}
</figure>

However, you want to change that. To modify, you go your previous script and add `min` `stepsize` `max` in `nxtransform`.   
I’ve provided an example of the script for general node lnx201. For clarity, I used the full path but you may want to modify it based on your directory structure and desired parameter values. Also, note that instead of using `nxreduce`, this workflow separates the process into two steps: `nxtransform` and `nxcombine`. In both cases, it is important that you `overwrite` the exsisting data.

!!! hint "Modification of the script"



                Comment out the below line
                #nxreduce --directory ${USER_DIR}${TEMP} --entries f1 f2 f3 --transform --combine --regular

                Add and modify below 
                nxtransform --directory /nfs/chess/id4baux/2023-3/sarker-3828-a/nxrefine/AB3C5/sample1/16/ --entries f1 f2 f3 -qh -8 0.01 8 -qk -8 0.01 8 -ql -18 0.01 18 --regular --overwrite

                and finally combine
                nxcombine --directory /nfs/chess/id4baux/2023-3/sarker-3828-a/nxrefine/AB3C5/sample1/16/ --entries f1 f2 f3 --regular --overwrite

After getting the data, visulize the HKLI and once you are satified with the stepsize, you set that as `parent file` again and reprocess rest of the dataset.
