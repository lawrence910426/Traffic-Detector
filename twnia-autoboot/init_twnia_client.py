import subprocess
import pyotp
import pexpect
import sys
import time

totp = pyotp.TOTP('7T3ORRWVOBQICTORGJ26ELYKNCRNJSEGFFQO5QDUEOZWRFZBEIOA====')

child = pexpect.spawn('ssh lawrence0426@ln01.twcc.ai')
child.logfile = sys.stdout.buffer

child.expect("Password: ")
out = child.sendline ("Lawrence Sean4011")

child.expect('Changing MOTP:')
out = child.sendline (totp.now())

child.expect('[lawrence0426@ln01-twnia2 ~]$')
out = child.sendline("cd /work/lawrence0426/Sharingan/twnia-autoboot; pgrep -x rev_shell_client || nohup bash init_twnia_rev_shell_client.sh; rm nohup.out")

time.sleep(3)
exit()

while True:
    try:
        child.expect ('\r\n')
    except:
        break

exit()
