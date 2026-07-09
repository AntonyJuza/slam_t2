import os

search_dir = '/home/juza/slam_t2/extracted_config/opt/ros/indigo/share/robot_settings/cfg/yaml/'
t2_files = sorted(os.listdir(os.path.join(search_dir, 'T2')))
t5_files = sorted(os.listdir(os.path.join(search_dir, 'T5')))

print("T2 configuration files:")
for f in t2_files:
    print(f" - {f}")
    
print("\nT5 configuration files:")
for f in t5_files:
    print(f" - {f}")
