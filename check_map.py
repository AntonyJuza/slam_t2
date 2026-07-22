import subprocess
res = subprocess.run(["docker", "exec", "rviz_opent2", "bash", "-c", "source /opt/ros/noetic/setup.bash && rostopic info /map"], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
