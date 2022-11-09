import subprocess
import pyotp
import pexpect
import sys
import time
import os

totp = pyotp.TOTP('7T3ORRWVOBQICTORGJ26ELYKNCRNJSEGFFQO5QDUEOZWRFZBEIOA====')

child = pexpect.spawn('ssh lawrence0426@ln01.twcc.ai')
child.logfile = sys.stdout.buffer

if 'init' in os.environ:
    child.expect(" (yes/no/[fingerprint])?")
    out = child.sendline ("yes")

child.expect("Password: ")
out = child.sendline ("Lawrence Sean4011")

child.expect('Changing MOTP:')
out = child.sendline (totp.now())

child.expect('[lawrence0426@ln01-twnia2 ~]$')
if 'init' in os.environ:
    out = child.sendline("pkill -f rev; exit")
else:
    out = child.sendline('cd /work/lawrence0426/Sharingan/twnia-autoboot; if [[ -z $(ps aux | grep -v "grep" | grep "init_twnia_rev_shell_client.sh") ]]; then bash init_twnia_rev_shell_client.sh; fi; rm nohup.out; exit')

time.sleep(5)

while True:
    try:
        child.expect ('\r\n')
    except:
        break

exit()
