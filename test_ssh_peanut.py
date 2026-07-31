import pexpect
import sys

print("=== TESTING SSH TO PEANUT@192.168.64.20 ===")
cmd = "ssh -o StrictHostKeyChecking=no peanut@192.168.64.20 'hostname; uptime; rosnode list 2>/dev/null || echo ROS_OFF'"

child = pexpect.spawn(cmd, encoding='utf-8', timeout=10)
idx = child.expect(['password:', pexpect.EOF, pexpect.TIMEOUT])
if idx == 0:
    child.sendline('root')
    child.expect(pexpect.EOF)
    print("SSH Output:\n" + child.before)
else:
    print(f"SSH Failed at index {idx}: " + child.before)
