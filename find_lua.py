import os

search_dir = '/home/juza/slam_t2/extracted_config'
lua_files = []

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.lua'):
            lua_files.append(os.path.join(root, file))

print(f"Found {len(lua_files)} .lua files:")
for f in lua_files:
    print(f.replace(search_dir, ""))
