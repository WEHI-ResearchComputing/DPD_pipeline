# https://bioinformatics.stackexchange.com/questions/13871/trying-to-download-a-large-number-of-files-from-ena-programmatically

#test edit

import queue
import threading
import time
from contextlib import closing
import shutil
import urllib.request as request
import pandas as pd
from csv import reader
import tarfile
import subprocess
import glob
import configparser
import time
import os
import sys

from Download import *
from Workflow import *
from Cleanup import *

config = configparser.ConfigParser()

config.read('config.ini')

ERRlist = config['ERRcodes']['list_location']
column_name = config['ERRcodes']['column_name']
md5_column = config['ERRcodes']['md5_column']
address = config['ENAdataget']['enadataget_path']
file_type = config['ENAdataget']['file_type']
output_path = config['outputs']['ERR_output_path']
logs = config['outputs']['log_outputs']
download_path = config['DownloadLocation']['download_path']
script = config['workflow']['script']
print(f'SCRIPT TYPE {type(script)}')
#script = script.encode(encoding='utf-8')
print(f'SCRIPT TYPE {type(script)}')
numThreads = config['threads']['thread_num']
numThreads = int(numThreads)
#print(f'NUM OF THREADS{numThreads}')

global dfCodesStates

class MyResume(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print('Starting resume thread %s.' % self.name)
        process_resume()
        print('Exiting resume thread %s.' % self.name)
        # print('sleeping for 1 second')
        time.sleep(1)

class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print('Starting thread %s.' % self.name)
        process_queue()
        print('Exiting thread %s.' % self.name)
        # print('sleeping for 1 second')
        time.sleep(1)

#Key for code state
#    0         1          2          3         4       5
# waiting downloading downloaded processed to remove  finished
def changeURLState(url, state):
    
    print(f'PRINTING url: {url} and state: {state}')
    
    count = 0
    
    # print(dfCodesStates)
        
    for code in dfCodesStates.iloc[:,0]:
        # print(f'{code} {url}')
        if code == url:
            # print('match')
            dfCodesStates.at[count, 1] = state
        count += 1

    # print(dfCodesStates)

    with open ('ERRs_and_codes.csv', 'w+') as states:
        dfCodesStates.to_csv(states, index=False)
        # print('written states to csv')

def process_queue():
    while True:
        try:
            url = my_queue.get(block=False)
            print(f'starting thread for {url}')
            # process = f'python C:/Users/Chris/Downloads/enaBrowserTools-0.0.3/enaBrowserTools-0.0.3/python3/enaDataGet.py {url}'

           
            print(f'downloading {url}')
            changeURLState(url, 1)
            if (download_then_check(url, address, download_path, logs, file_type, md5_column, ERRlist, column_name)):
                changeURLState(url, 2)
                print(f'sending {url} to workflow')
                script_workflow(url, download_path, logs, script)
                    # changeURLState(url, 3)
                    # print(f'cleaning up {url}')
                    # changeURLState(url, 4)
                    # if (clean(url, download_path, logs)):
                    #     changeURLState(url, 5)
                    #write_in_process(to_download, to_process, to_delete)

        except queue.Empty:
            print('q empty')
            return

# setting up variables
# read in the file names of the samples we need
samples = pd.DataFrame(columns=['sample', 'study', 'site', 'country', 'lat', 'long', 'year', 'ENA', 'allSamplesSameIndividual', 'population', 'percentCallable', 'QCpass', 'exclusion', 'isReturningTraveller'])

downloaded_urls = ['ERR1081239','ERR1081240', 'ERR021984','ERR021985','ERR022863','ERR022864','ERR022865','ERR022866','ERR022867','ERR023039','ERR023040','ERR023041']

csv_urls = ['ERR1081237','ERR1081238','ERR1081239','ERR1081240', 'ERR021984','ERR021985','ERR022863','ERR022864','ERR022865','ERR022866','ERR022867','ERR023039','ERR023040','ERR023041']

urls = []

resume_threads = []

def process_resume():
    while True:
        try:
            url = my_queue.get(block=False)
            print(f'starting resume for {url}')
            for row in range (0, len(dfCodesStates)):
                if (url == dfCodesStates.iloc[row, 0]):
                    if (dfCodesStates.iloc[row, 1] == 0):
                        # print('state is 0')
                        urls.append(dfCodesStates.iloc[row, 0])
                    if (dfCodesStates.iloc[row, 1] == 1):
                        # print('state is 1')
                        clean_download(os.path.join(download_path, dfCodesStates.iloc[row, 0]))
                        if(download_then_check(dfCodesStates.iloc[row, 0], address, download_path, logs, file_type, md5_column, ERRlist, column_name)):
                            changeURLState(url, 2)
                            if(script_workflow(dfCodesStates.iloc[row, 0], download_path, logs, script)):
                                changeURLState(url, 3)
                                print(f'cleaning up {url}')
                                changeURLState(url, 4)
                                if (clean(url, download_path, logs)):
                                    changeURLState(url, 5)
                    if(dfCodesStates.iloc[row, 1] == 2):
                        # print('state is 2')
                        if(script_workflow(dfCodesStates.iloc[row, 0], download_path, logs, script)):
                            changeURLState(url, 3)
                            print(f'cleaning up {url}')
                            changeURLState(url, 4)
                            if (clean(url, download_path, logs)):
                                changeURLState(url, 5)
                    if (dfCodesStates.iloc[row, 1] == 3):
                        # print('state is 3')
                        changeURLState(url, 4)
                        if (clean(url, download_path, logs)):
                            changeURLState(url, 5)
                    if (dfCodesStates.iloc[row, 1] == 4):
                        # print('state is 4')
                        if (clean(url, download_path, logs)):
                            changeURLState(url, 5)
                    if (dfCodesStates.iloc[row, 1] == 5):
                        print('state is 5, code has been processed, nothing to do')
        except queue.Empty:
            print('q empty')
            return

#Key for code state
#    0         1          2          3         4       5
# waiting downloading downloaded processed to remove  finished

#working on each case individually instead of putting them all into lists then working on the whole list
def compare_lists(df_toDL):
    toDL_codes = df_toDL[column_name]
    #print(f'CODES {toDL_codes}')
    if (os.path.exists('ERRs_and_codes.csv')):
        with open ('ERRs_and_codes.csv', 'r+') as codes:
            global dfCodesStates
            dfCodesStates = pd.read_csv('ERRs_and_codes.csv')
            for row in range (0, len(dfCodesStates)):
                # print(dfCodesStates.iloc[row, 0])
                resume_threads.append(dfCodesStates.iloc[row, 0])
            start_resume()
                
    else:
        dfCodesStates = pd.DataFrame()
        for url in toDL_codes:
            # print(url)
            urls.append(url)
            dfCodesStates = dfCodesStates.append([[url, 0]], ignore_index=True)
            # print(f'adding {url} to the dataframe')
            # print(dfCodesStates)
    
    # for url in range (0, len(toDL_codes)):
    #     if toDL_codes[url] not in urls:
    #         urls.append(toDL_codes[url])
            #also remove urls in to_process and to_delete
    
    # print(urls)
    #return dfCodesStates

def read_codes():

    df_toDL = pd.read_csv(ERRlist)
    # print(df_toDL)
    codes_column = df_toDL[column_name]

    # for code in codes_column:
    #     print(f'READING THIS {code} FROM THE TEST CSV')
    #     urls.append(code)
        

    #print(urls)
    return df_toDL

my_queue = queue.Queue()

def start_resume():
    # filling the queue
    #my_queue = queue.Queue()

    # for url in urls:py    
    #     urls_txt.write(url)

    for url in resume_threads:
        
        my_queue.put(url)

    # initializing and starting num_threads threads
    num_threads = numThreads
    threads = []

    for i in range(num_threads):
        thread = MyResume(i)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def start_threads():
    # filling the queue
    #my_queue = queue.Queue()

    # for url in urls:py    
    #     urls_txt.write(url)

    for url in urls:
        
        my_queue.put(url)

    # initializing and starting num_threads threads
    num_threads = numThreads
    threads = []

    for i in range(num_threads):
        thread = MyThread(i)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def create_output_folder(file):
    try:
        if (os.path.exists(file) == False):
            os.mkdir(file)
        else: return
    except Exception as e:
        print(e)
        sys.exit(f"Cannot create {file} output file, logs are required, fix this issue and re-run")

def main():
    df_toDL = read_codes()
    create_output_folder(logs)
    create_output_folder(output_path)
    create_output_folder(download_path)
    compare_lists(df_toDL)
    #changeURLState('ERR1081239', 4)

    # #print(urls)
    start_threads()
    print('program done')

main()