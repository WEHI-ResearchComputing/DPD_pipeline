import os
import sys
import shutil

def clean_logs(logs):
    try:
        shutil.rmtree(logs)
        make_loc(logs)
    except Exception as e:
        print(e)
        print('cannot remove logs')
        
def clean_outputs(output_location):
    try:
        shutil.rmtree(output_location)
        make_loc(output_location)
    except Exception as e:
        print(e)
        print('cannot remove outputs')

def clean_download(download_location):
    try:
        shutil.rmtree(download_location)
    except Exception as e:
        print(e)
        print('cannot remove past downloads')

def clean_downloads_location(download_location):
    try:
        shutil.rmtree(download_location)
        make_loc(download_location)
    except Exception as e:
        print(e)
        print('cannot remove past downloads')

def open_files(logs):
    global failed_to_delete 
    failed_to_delete = open(f'{logs}/failed_to_delete.txt', 'a')

def clean(url, output_path, logs):
    
    open_files(logs)
    
    try:
        shutil.rmtree(os.path.join(output_path, url))
        print(f'{url} workflow removed')
        return True
    except Exception as e:
        failed_to_delete.write(f'the folder {url} and its contents could not be deleted - {e.strerror}')
        print('bad')
    except:
        print('bad')

def make_loc(location):
    try:
        os.mkdir(location)
    except:
        print('cannot make folder')
#need to add a pass through of the ouput folder
# def main():
#     clean('ERR_outputs\ERR426135')
# main()
