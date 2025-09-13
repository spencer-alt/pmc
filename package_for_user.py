#!/usr/bin/env python3
"""
Create a complete downloadable package for the user
"""

import os
import shutil
import zipfile

def create_user_package():
    """Create a zip package with all necessary files for the user"""
    
    package_name = "polymarket_local_executor"
    
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    files_to_copy = [
        'setup.py',
        'local_executor.py', 
        'requirements.txt',
        '.env.template',
        'README_LOCAL_EXECUTOR.md'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
            print(f"✓ Copied {file}")
        else:
            print(f"✗ Missing {file}")
    
    zip_filename = f"{package_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
                print(f"✓ Added {arcname} to zip")
    
    print(f"\n✓ Package created: {zip_filename}")
    print(f"Package size: {os.path.getsize(zip_filename)} bytes")
    
    shutil.rmtree(package_name)
    
    return zip_filename

if __name__ == "__main__":
    create_user_package()
