#!/usr/bin/env python3
import os
import sys
import zipfile
import re
from datetime import datetime
import argparse
import shutil
import tempfile

def get_version():
    """Get version from __init__.py"""
    with open('__init__.py', 'r') as f:
        content = f.read()
        match = re.search(r'"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
        if match:
            return tuple(map(int, match.groups()))
    return (0, 0, 0)

def update_version(major=False, minor=False, patch=True):
    """Update version in __init__.py"""
    current_version = get_version()
    
    if major:
        new_version = (current_version[0] + 1, 0, 0)
    elif minor:
        new_version = (current_version[0], current_version[1] + 1, 0)
    elif patch:
        new_version = (current_version[0], current_version[1], current_version[2] + 1)
    else:
        new_version = current_version
    
    # Read the file
    with open('__init__.py', 'r') as f:
        content = f.read()
    
    # Update version
    new_version_str = f'({new_version[0]}, {new_version[1]}, {new_version[2]})'
    content = re.sub(
        r'"version":\s*\(\d+,\s*\d+,\s*\d+\)',
        f'"version": {new_version_str}',
        content
    )
    
    # Write back to file
    with open('__init__.py', 'w') as f:
        f.write(content)
    
    print(f"Updated version to {'.'.join(map(str, new_version))}")
    return new_version

def create_release(major=False, minor=False, patch=True):
    # Update version if needed
    version = update_version(major, minor, patch)
    version_str = '.'.join(map(str, version))
    
    # Create zip filename with version and date
    date = datetime.now().strftime('%Y%m%d')
    zip_name = f'bake_tools_addon_v{version_str}_{date}.zip'
    
    # Ensure releases directory exists
    releases_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'releases')
    os.makedirs(releases_dir, exist_ok=True)
    
    # Full path for the zip file
    zip_path = os.path.join(releases_dir, zip_name)
    
    # Files to exclude
    exclude = [
        '.DS_Store',
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.git',
        '.gitignore',
        'scripts',
        '*.zip',
        'releases'  # Exclude the releases directory itself
    ]

    # Create a temporary directory for packaging
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the addon directory inside temp_dir
        addon_dir = os.path.join(temp_dir, 'bake_tools_addon')
        os.makedirs(addon_dir)
        
        # Copy files to the temporary directory
        for root, dirs, files in os.walk('.'):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude and not any(ex in d for ex in exclude)]
            
            for file in files:
                # Skip excluded files
                if any(ex in file for ex in exclude):
                    continue
                
                # Get source and destination paths
                src_path = os.path.join(root, file)
                # Remove the leading './' from the root path
                rel_path = os.path.relpath(src_path, '.')
                dst_path = os.path.join(addon_dir, rel_path)
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy the file
                shutil.copy2(src_path, dst_path)
        
        # Create zip file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
    
    print(f"Created release: {zip_path}")
    return zip_path

def main():
    parser = argparse.ArgumentParser(description='Create a new release of the bakery addon')
    parser.add_argument('--major', action='store_true', help='Increment major version')
    parser.add_argument('--minor', action='store_true', help='Increment minor version')
    parser.add_argument('--patch', action='store_true', help='Increment patch version (default)')
    
    args = parser.parse_args()

    create_release(args.major, args.minor, args.patch)

if __name__ == '__main__':
    main() 