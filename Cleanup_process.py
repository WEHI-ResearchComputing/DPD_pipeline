import os
import sys
import shutil
import pandas as pd

url = sys.argv[1]
download_path = sys.argv[2]
logs = sys.argv[3]

def write_to_log(logs, log):
    with open(f'{logs}/failed_to_delete.txt', 'a') as f:
        f.write(log)

def changeURLState(url, state):
    with open ('ERRs_and_codes.csv', 'r') as states:
        dfCodesStates = pd.read_csv('ERRs_and_codes.csv')
        # print('written states to csv')
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

def clean(url, download_path, logs):
    changeURLState(url, 4)
    try:
        shutil.rmtree(os.path.join(download_path, url))
        print(f'{url} workflow removed')
        return True
    except Exception as e:
        write_to_log(logs, '{url} download folder and contents could not be deleted - {e}')

def main(url, download_path, logs):
    changeURLState(url, 3)
    if (clean(url, download_path, logs)):
        changeURLState(url, 5)

main(url, download_path, logs)