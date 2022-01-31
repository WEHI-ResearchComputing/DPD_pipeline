import hashlib
import xml.etree.ElementTree as ET
import os
import glob
import subprocess
import gzip
import pandas as pd

#get file thats created url, searches for .cram or .bam files. Returns true if glob returns something
#glob returns a list so need to access the first index of it
def get_crambam(url, download_path):
    if(glob.glob(f'{download_path}/{url}/*.cram')):
        result = glob.glob(f'{download_path}/{url}/*.cram')
        # print('can find cram')
        return result[0]
    if(glob.glob(f'download_path/{url}/*.bam')):
        result = glob.glob(f'download_path/{url}/*.bam')
        # print('can find bam')
        return result[0]
    else: 
        # print('cant find')
        write_to_unavil(logs, f'{url} is not in bam or cram format')
        return False

#allows to find any compression of fastq files
def get_fastq(url, download_path, logs):
    # print(glob.glob(f'{download_path}/{url}/*.fastq.*'))
    if(glob.glob(f'{download_path}/{url}/*.fastq.*')):
        result = glob.glob(f'{download_path}/{url}/*.fastq.*')
        # print(result)
        # print('can find cram')
        return result[0]
    else: 
        print('cant find')
        write_to_unavil(logs, f'{url} is not in fastq.gz format')
        return False        

#making sure the file exists
def check_exists(url, download_path):
    try:
        #trying to find a file with the .cram or .bam extension
        result = get_crambam(url, download_path)
        # print(result)
        if (os.path.exists(result)):
            print(f'{url} dir exists True')
            return(True)
    except:
        print(f'{url} exists false')
        return(False)
        
def check_exists_fastq(url, download_path, logs):
    # print(glob.glob(f'{download_path}/{url}/*.fastq.gz'))
    try:
        #trying to find a file with the .cram or .bam extension
        result = get_fastq(url, download_path, logs)
        # print(result)
        if (os.path.exists(result)):
            print(f'{url} dir exists True')
            return(True)
    except:
        print(f'{url} exists false')
        return(False)

def gzip_md5(fname):
    hash_md5 = hashlib.md5()
#     print(fname)
    with gzip.open(fname, "r") as f:
        fr = f.read()
        hash_md5.update(fr)
#     print(to_return)
    return hash_md5.hexdigest()


#calculating the md5 checksum
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_csv_md5(url, ERRlist, md5_col, code_column_name, logs):
    with open (ERRlist, 'r+') as codes:
        count = 0
        print(count)
        codes_for_csv = pd.read_csv(codes)
        md5_column = codes_for_csv[md5_col]
        code_column = codes_for_csv[code_column_name]
        for row in codes_for_csv:
            if code_column[count] == url:
                md51, md52 = md5_column[count].split(';')
                print(md51)
                print(md52)
                return md51, md52
            count += 1

#parsing the xml file that comes with the file
def get_xml_md5(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    c = root.find("RUN/DATA_BLOCK/FILES/FILE")
    result = c.get('checksum')
    return result

#comparing the md5 results

def compare(file, xml):
    if file == xml:
        print(f'{file} valid')
        return True
    else:
        print(f'{file} corrupt')
        return False

#if one is corrupt then it returns false since both are needed to align
def check_fastq_md5(url, download_path, md5_column, ERRlist, code_column_name, logs):
    # print(url+ download_path+ md5_column+ ERRlist +code_column_name)
    if(check_exists_fastq(url, download_path, logs)):
        one = False
        two = False
        md51, md52 = get_csv_md5(url, ERRlist, md5_column, code_column_name, logs)
        print(md51)
        print(md52)
        # with gzip.open(f'{download_path}/{url}/{url}_1.fastq.gz') as f: 
        # print('opened 1')
        f_md5 = gzip_md5(f'{download_path}/{url}/{url}_1.fastq.gz')
        if (compare(f_md5, md51)):
            print('file 1 and csv md5 the same')
            write_to_success(logs, f'{url}_1 successfully downloaded and md5 checked\n')
            one = True 
        else: print('file 2 and csv md5 NOT the same')
        # with gzip.open(f'{download_path}/{url}/{url}_2.fastq.gz') as f:
        print('opened 2')
        f_md5 = gzip_md5(f'{download_path}/{url}/{url}_2.fastq.gz')
        if (compare(f_md5, md52)):
            write_to_success(logs, f'{url}_2 successfully downloaded and md5 checked\n')
            two = True 
        else: print('file 2 and csv md5 NOT the same')
        return one and two
    else: print('file 2 doesnt appear to exist')

#change 
def check_cram_md5(url, download_path, logs):
    if check_exists(url, download_path, logs):
        cram_file = get_crambam(url, download_path)
        file_md5 = md5(cram_file)
        xml_md5 = get_xml_md5(f'{download_path}/{url}/{url}.xml')
        if(compare(file_md5, xml_md5)==True):
            write_to_success(logs, f'{url} successfully downloaded and md5 checked\n')
            print(f'{url} successfully downloaded and md5 checked')
            return(True)
        else: 
            print(f'{url} is corrupt, md5 does not match')
            write_to_fail(logs, f'{url}\n')
            return False
    else:
        fail_file.write(f'{url}\n')
        print(f'{url} file doesnt exist')
        return(False)

def download_file_asp(url, address, download_path, logs):
    try: 
        print(f'trying to download {url}')
        process = subprocess.run(["python3", address, "-d", download_path, "-a", "-m", f"{url}"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #print(f'{url} out and err')
        # print(stdout)
        # print(stderr)
    except process.stderr == 'ERROR: Invalid accession provided\r\n':
        write_to_unavil(logs, f'{url} has an invalid accession code\n')
        print(f'{url} unavailable/incorrect code')
        return 0
    except subprocess.CalledProcessError as e:
        print(f'{url} failed')
        return False
    else: return 1

def download_file_ena(url, address, download_path, f_type, logs):
    try: 
        #print(url)
        # print(f'trying to download {url}')
        if f_type =='':
            process = subprocess.run(["python3", address, "-d", download_path, "-m", url], stdout=subprocess.PIPE,stderr=subprocess.PIPE) #, "-d", download_path
            return 'cram'
        else:
            #embl,fasta,submitted,fastq,sra
            process = subprocess.run(["python3", address, "-f", f_type, "-d", download_path, "-m", url], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            return 'fastq'
        #print(f'{stdout}, {stderr}')
    except process.stderr == 'ERROR: Invalid accession provided\r\n':
        write_to_unavil(logs, f'{url} has an invalid accession code\n')
        print(f'{url} unavailable/incorrect code')
        return 0
    except subprocess.CalledProcessError as e:
        print(f'{url} failed')
        return False
    #else: return 1

# def download_file(url, address):
#     process = subprocess.run(["python", address, "-m", f"{url}"], shell = True, capture_output=True)
#     if (process.stderr == 'ERROR: Invalid accession provided\r\n'):
#         file_unavailable.write(f'{url} has an invalid accession code')
#         print('unavailable/incorrect code')
#         return 0
#     if (check_exists(url)):
#         return True
#     else: 
#         return False

# def download_then_check(url, address):
#     count = 0
#     while count < 3:
#         print(f'try number {count+1}')
#         check = download_file(url, address)
#         try:
#             result = check_file_md5(url)
#         except check == 0 :
#             fail_file.write(f'{url} is an incorrect accession code')
#             print('Sample not available')
#             return False
#         except check == False :
#             count += 1
#             print('Sample not available')
#         else: 
#             count = 3        
#             return result

def write_to_success(logs, log):
    with open(f'{logs}/file_check_successes.txt', 'a') as f:
        f.write(log)
def write_to_failed(logs, log):
    with open(f'{logs}/files_failed.txt', 'a') as f:
        f.write(log)
def write_to_unavil(logs, log):
    with open(f'{logs}/file_unavailable.txt', 'a') as f:
        f.write(log)

# def open_files(logs):
#     global success_file 
#     success_file = open(f'{logs}/file_check_successes.txt', 'a')
#     global fail_file 
#     fail_file = open(f'{logs}/files_failed.txt', 'a')
#     global file_unavailable 
#     file_unavailable = open(f'{logs}/file_unavailable.txt', 'a')
    
def download_then_check(url, address, download_path, logs, file_type, md5_column, ERRlist, column_name):
    # open_files(logs)
    count = 0
    while count < 3:
        print(f'try number {count+1} for {url}')
        to_return = 0
        if(download_file_ena(url, address, download_path, file_type, logs) == 'cram'):
            count = 3
            to_return = check_cram_md5(url, download_path, logs)
            return to_return
        if(download_file_ena(url, address, download_path, file_type, logs) == 'fastq'):
            count = 3
            to_return = check_fastq_md5(url, download_path, md5_column, ERRlist, column_name, logs)
            return to_return
        if(download_file_ena(url, address, download_path, file_type, logs) == 0):
            write_to_fail(logs, f'{url} is an incorrect accession code\n')
            print('Sample not available')
            return False
        if(download_file_ena(url, address, download_path, file_type, logs) == False): 
            count += 1
            print('Sample not available')
    else: 
        print(f'{url} has been tried 3 times and cannot be downloaded')
        write_to_fail(logs, f'{url} has been tried 3 times and cannot be downloaded')
        return False


# ############all code below here needs to be commented out, for testing only
# address = "C:/Users/Chris/Downloads/enaBrowserTools-0.0.3/enaBrowserTools-0.0.3/python3/enaDataGet.py"
# #ERR426135

# def test_all():
#     download_then_check('ERR425', address)

# def test_checks():
#     check_file_md5('ERR426135')

# def main():
#     #test_all()
#     test_checks()

# main()