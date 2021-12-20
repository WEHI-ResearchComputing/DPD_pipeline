import subprocess

process = subprocess.run(["python3", '/home/users/allstaff/bollands.c/scratch/bollands.c/Malaria_downloads/enaBrowserTools-0.0.3/enaBrowserTools-0.0.3/python3/enaDataGet.py', "-a", "-m", "ERR1081237"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

print(process.stderr)

# if process.stderr != None:
#     print(process.stderr)