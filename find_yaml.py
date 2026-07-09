import os

search_dir = '/home/juza/slam_t2/extracted_config'
matches = []

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file == 'location_fusion.yaml':
            matches.append(os.path.join(root, file))

print(f"Found {len(matches)} files:")
for m in matches:
    print(m.replace(search_dir, ""))
