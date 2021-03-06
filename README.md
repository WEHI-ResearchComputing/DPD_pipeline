### to add
More user testing is required now

# Malaria CNV Pipeline
This github contains code for a pipeline to assist with the downloading, processing and removal of bulk samples from ENA. This program takes input from a CSV (comma separated file) and a config.ini file. The CSV is to contain the sample codes and the config is to contain the processing information, more information below. The program will download the files given, check them against the md5s to make sure they are not corrupt. The program with then send them to the script that the user provides for processing. This will create another 2 slurm jobs, one that runs the script provided and one that waits for the processing script to be completed which then runs the cleanup_process.py. This removes the downloaded files to save space on the system.

<img width="1016" alt="Screen Shot 2022-02-02 at 12 47 34 pm" src="https://user-images.githubusercontent.com/13778200/152080762-09d9ce3f-a711-447c-bead-c9304c6d58d5.png">


### Contains
App.py - controls the threading and the ENA accession codes to be downloaded and processed

Download.py - controls the download and the file md5 checks

Workflow.py - contains the sample workflow at the moment

Cleanup.py and Cleanup_process.py - removes the download folders at the end of the workflow

## Install ENA data get and set up a conda env
download enaDataGet from https://github.com/enasequence/enaBrowserTools. Locate and make note of the location

```
git clone https://github.com/WEHI-ResearchComputing/DPD_pipeline.git
cd DPD_pipeline
module load anaconda3
conda init
conda create --name my_pipeline --file requirements.txt
```

## Config file
for a bash script to correctly read a .ini file, there must be no spaces in the deleration of locations. E.g
list_location=test.csv
not
list_location = test.csv
Edit config.ini through a text editor or on demand, example:

```
[ERRcodes]
list_location=test.csv
column_name=run_accession
md5_column=fastq_md5

[DownloadLocation]
download_path=/home/users/allstaff/bollands.c/scratch/bollands.c/Malaria_downloads

[ENAdataget]
enadataget_path=/home/users/allstaff/bollands.c/scratch/bollands.c/Malaria_downloads/enaBrowserTools-0.0.3/enaBrowserTools-0.0.3/python3/enaDataGet.py
file_type=fastq

[outputs]
ERR_output_path=/vast/scratch/users/bollands.c/ERR_outputs
log_outputs=./logs

[threads]
thread_num=3

[workflow]
script=/stornext/HPCScratch/home/bollands.c/Malaria_downloads/jocelyn_scripts/fastq2bamVivax.sh
```
requires n>2 threads for the resumability to work with threading


change the **absolute address** of all the different config file targets


## ERR list file
This is the file that contains the accession codes of all the samples that you wish to download. To maintain accuracy, the program uses the md5 checksum of the file to determine if the file is corrupt or not. This requires the user to supply the known md5 checksum for a reference. Using ERR codes, this can be found by following this link and following the instructions - https://ena-docs.readthedocs.io/en/latest/retrieval/programmatic-access/file-reports.html. This will generate a list of the codes and the md5s for the given project.

## Script
The code is configured so that when the user runs the pipeline with a script workflow, the code runs the script and sends the location of the working sample to it and the accession code of the sample itself. Therefore, the users script must be able to take the location of the file and work with that. Example location and sample

/stornext/HPCScratch/home/bollands.c/Malaria_downloads/ERR12345/ERR12345(.fastq/whatever file type you have requested to download, your script must specify this)

Adding for example
```
f1=${1}'_1.fastq.gz'
```
into your sh script means its taking in the first argument that you are passing to the code. It is possible to add as many as you want but you cannot use {0} as that references the script itself.

Combining the example location and variable example gives the entire path and name of the file that has just been downloaded and can now be processed with your script.

If there are multiple steps to your workflow please configure a script to be called that can handle that as the workflow calls one script only.

## Running
In SLURM run the following command
```
sbatch pipelineScript.sh
```
## How to interpret outputs
ERRs_and_codes.csv is created in the same folder that contains the App.py as a way of keeping track of the state of different accession codes. Column 1 is the accession code and column 2 is the state that the code is in.

```
Key for code state
   0         1          2          3         4       5
waiting downloading downloaded processed to remove  finished
```


