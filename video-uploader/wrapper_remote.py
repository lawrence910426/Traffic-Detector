import subprocess
import pexpect
import sys
import time

child = None

def func1():
    global child

    child = pexpect.spawn("nc localhost 8787")
    child.logfile = sys.stdout.buffer

    child.expect("[lawrence0426@ln01-twnia2 ~]$")
    child.sendline('module load miniconda3 && conda activate youtube-upload && cd /work/lawrence0426/Sharingan/video-uploader/ && python youtube.py --file 30sec.MOV')

    child.expect_exact("Please visit this URL to authorize this application: ")
    line = child.readline(1)
    print(line)

def func2():
    global child

    child.expect_exact("Enter the authorization code: ")
    out = child.sendline("qwer")

    child.expect_exact("Youtube link: ")
    line = child.readline(1)
    print(line)

while True:
    if input() == '1':
        func1()
    else:
        func2()
