


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
Make sure you have permission for the desired folders,  before running the job in the queue, ask your beamline scientist to change the permission of the folder (it is always need to be updated). Also, make sure you have the <i> parent file </i> for each folders, otherwise the code will not work. </b>

!!! danger "Change the < classe_id > to your own CLASSE ID" 

* (ii) <b> Step 2 :</b> Login to lnx201

        ssh <classe_id>@lnx201.classe.cornell.edu

* (iii) <b> Step 3 :</b> Make sure you are at home directory

        cd 
        pwd
        /home/<classe_id>/

* (iv) <b> Step 4 :</b> create nxserver settings

        mkdir -p  /home/<classe_id>/.nxserver/


* (v) <b> Step 5 :</b>: Copy the nxserver setting


        cp /home/ss3428/.nxserver/settings.ini /home/<classe_id>/.nxserver/

* (vi) <b> Step 6 :</b>: Go to the desired data analayis forder (it will your folder in aux)

        cd /nfs/chess/id4baux/2024-1/<BTR-3946-a>/


* (vi) <b> Step 7 :</b>: Changed the desired steps for nxrefine from the folder or if you know how to use vim, then do to change the qsub file and do that necessasy steps 

* Make sure you have change the file path and the threshold of the nxfind of the sample

* If you are nomachine, you can change the qsub_jobs_****.sh file directly based on the steps you want to perform in the data processing  

        vim qsub_jobs_<name of the user>.sh 


* (vii) <b> Step 8 : </b> Run the job in lnx201 (make sure path is correct)

        qsub -q all.q -l mem_free=350G -pe sge_pe 8 -hold_jid 8 -S /bin/bash /nfs/chess/id4baux/2024-1/postec-3946-a/qsub_jobs_<name of the file>.sh

!!! danger "If it did not work, try to use less memory and submit the job again" 
* You can change mem_free = 200, below is the example
        
        qsub -q all.q -l mem_free=200G -pe sge_pe 8 -hold_jid 8 -S /bin/bash /nfs/chess/id4baux/2024-1/postec-3946-a/qsub_jobs_<name of the file>.sh



* (viii) <b> Step 9 :</b> Check the status

        qstat


* (ix) <b> Step 10 :</b> See the status ebaborately


        cat qsub_jobs_<classe_id>.sh.e7231424

* (x) <b> Step 11 :</b> Finally after you the data procesing


        cd /nfs/chess/id4baux/2024-1/
        chmod -R 777 <project_name>