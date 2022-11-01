import subprocess
import pexpect
import sys
import time
import pickle
import argparse
import dill

child = pexpect.spawn('python3 youtube.py')
# child.logfile = sys.stdout.buffer

child.expect_exact("Please visit this URL to authorize this application: ")
line = child.readline(1)
print(line)

child.expect_exact("Enter the authorization code: ")
out = child.sendline (input())

child.expect_exact("Youtube link: ")
line = child.readline(1)
print(line)

