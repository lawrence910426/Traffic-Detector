import subprocess
import pexpect
import sys
import time
import pickle
import argparse
import dill

parser = argparse.ArgumentParser("Youtube wrapper")
parser.add_argument(
    "--step", 
    help="Either `url` for retrieve url or `auth` for apply authentication code", 
)
args = parser.parse_args()

if args.step == 'url':
    child = pexpect.spawn('python3 youtube.py')
    # child.logfile = sys.stdout.buffer

    child.expect_exact("Please visit this URL to authorize this application: ")
    line = child.readline(1)
    print(line)

    handle = dill.dumps(child)

if args.step == 'auth':
    child = dill.loads(handle)

    child.expect_exact("Enter the authorization code: ")
    out = child.sendline (input())

    child.expect_exact("Youtube link: ")
    line = child.readline(1)
    print(line)

