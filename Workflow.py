import os
import sys
import subprocess

#OUTPUT_LOCATION = 'ERR_outputs'

def create_folder(url, output_location):
    os.mkdir(os.path.join(output_location, url))
    success_file.write(f'{os.path.join(output_location, url)}\n')
    # print(f'created {url} folder')

#change the batch.bat to a variable that is passed through the config file
#add subprocess scripts and what inputs/outputs. Need outputs that tell us if the work
def script_workflow(url, download_path, logs, script):
    success_file = open(f'{logs}/workflow_success.txt', 'a')
    # print(f'attempting to run {url}, script: {script}')
    path = f'{download_path}/{url}/{url}'
    process = subprocess.run(["dsbatch", f"{script}", f'{path}'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process_id = process.stdout
    process_id = process_id.decode('ascii')
    process_id = process_id.rstrip('\n')
    on_success = subprocess.run(["sbatch", f"--dependency=afterok:{process_id}", "cleanup_job.sh", url, download_path, logs])
    # shell = True, input=path, universal_newlines=True,capture_output=True, encoding='utf-8'
    #process.stdin.write(f'{url}')
    print(f'{url}: STDOUT: {process.stdout}. STERR: {process.stderr}')
    # print('THIS IS AFTER RUNNING DA SCRIPT')
    if process.returncode == 0:
    #     print(has)
    # if (process.stderr == b''):
        return True
    else: return False

def open_files(logs):
    global success_file 
    success_file = open(f'{logs}/workflow_success.txt', 'a')

#creating empty folder for testing, maybe change to subproccess
def file_workflow(url, output_location, logs):
    open_files(logs)
    #print(f'{output_location}')
    try: 
        if (os.path.exists(f'{output_location}') == False):
            try: 
                # print(f'trying to make outputs folder')
                os.mkdir(f'{output_location}')
                if (os.path.exists(output_location)):
                    create_folder(url, output_location)
                    return True
            except Exception as e:
                print(e)
                print(f'{url} Could not create directory')
                return False
            except:
                return False
        else:
            create_folder(url, output_location)
            return True
    except Exception as e:
        print(e)
        print(f'{url} No permissions to access file')
        return False

# def main():
#     workflow('ERR426135')

# main()