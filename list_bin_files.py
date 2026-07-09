import zipfile

zip_path = '/home/juza/keenon_ros.zip'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    all_files = zip_ref.namelist()
    
    bin_files = []
    for f in all_files:
        if 'lib/chassis' in f or 'lib/location_fusion' in f or 'lib/peanut_localization' in f:
            bin_files.append(f)
            
    print(f"Found {len(bin_files)} files related to chassis/localization:")
    for f in bin_files[:50]:
        print(f)
