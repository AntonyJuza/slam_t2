import zipfile
import os

zip_path = '/home/juza/keenon_ros.zip'
dest_dir = '/home/juza/slam_t2/extracted_config'

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

print("Opening zip file...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    all_files = zip_ref.namelist()
    print(f"Total files in zip: {len(all_files)}")
    
    target_files = []
    for f in all_files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.lua', '.launch', '.yaml']:
            target_files.append(f)
            
    print(f"Found {len(target_files)} target configuration files (.lua, .launch, .yaml).")
    
    # Extract them
    for f in target_files:
        try:
            zip_ref.extract(f, dest_dir)
        except Exception as e:
            print(f"Error extracting {f}: {e}")

print("Extraction completed!")
