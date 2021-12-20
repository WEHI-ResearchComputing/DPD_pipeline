### to add
Resumability testing - code is there just needs to be un-commented
Resumability run through threading as well to make it more efficient rather than dealing with the codes on a case by case basis

# Malaria CNV Pipeline
This github contains the code for a pipeline to assist with the download, processing and removal of bulk Malaria samples from ENA. This program takes input from a CSV (comma separated file), it does not read anything else yet. It is important that your input file is of type CSV.

### Contains
App.py - controls the threading and the ENA accession codes to be downloaded and processed

Download.py - controls the download and the file md5 checks

Workflow.py - contains the sample workflow at the moment

Cleanup.py - removes the workflow folders

## Install ENA data get and set up a conda env
download enaDataGet from https://github.com/enasequence/enaBrowserTools. Locate and make note of the location

```
git clone https://github.com/WEHI-ResearchComputing/Malaria_CNV_Pipeline
cd Malaria_CNV_Pipeline
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
column_name=ERR

[DownloadLocation]
download_path=/vast/scratch/users/bollands.c/ERR_downloads

[ENAdataget]
enadataget_path=/home/users/allstaff/bollands.c/scratch/bollands.c/Malaria_downloads/enaBrowserTools-0.0.3/enaBrowserTools-0.0.3/python3/enaDataGet.py

[outputs]
ERR_output_path=/vast/scratch/users/bollands.c/ERR_outputs
log_outputs=./logs

[threads]
```
requires n>2 threads for the resumability to work with threading
```
thread_num=3
 ```

change the **absolute address** of the csv containing accession codes, the name of the column containing the accession codes, location for the samples to be downloaded to, location of the enaDatGet program, location for the workflow output and the number of threads.

## Running
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


