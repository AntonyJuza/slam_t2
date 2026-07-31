import pexpect
import sys

print("=== VERBOSE SSH TEST ===")
child = pexpect.spawn("ssh -v -o StrictHostKeyChecking=no peanut@192.168.64.20", encoding='utf-8', timeout=8)
child.logfile = sys.stdout
child.expect([pexpect.EOF, pexpect.TIMEOUT])
