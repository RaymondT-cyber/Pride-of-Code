"""
Build Package Script - Create distributable packages for Code of Pride.

This module creates distributable packages for different platforms.
"""

import os
import sys
import shutil
import zipfile
import tarfile
from pathlib import Path

def create_directory_structure():
    """Create the directory structure for the distributable package."""
    # Create base directory
    base_dir = "code-of-pride-dist"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)
    
    # Create subdirectories
    dirs = [
        "assets",
        "core",
        "docs",
        "gameplay",
        "scenes",
        "story",
        "tests",
        "ui",
        "audio",
        "config"
    ]
    
    for dir_name in dirs:
        os.makedirs(os.path.join(base_dir, dir_name), exist_ok=True)
        
    return base_dir

def copy_files(base_dir):
    """Copy necessary files to the distribution directory."""
    # Files to copy
    files_to_copy = [
        "config.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        "run.sh",
        "DEMO.py"
    ]
    
    # Copy files
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            shutil.copy2(file_path, os.path.join(base_dir, file_path))
    
    # Copy directories
    dirs_to_copy = [
        "assets",
        "core",
        "docs",
        "gameplay",
        "scenes",
        "story",
        "tests",
        "ui",
        "audio"
    ]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(base_dir, dir_name), dirs_exist_ok=True)

def create_startup_scripts(base_dir):
    """Create platform-specific startup scripts."""
    # Windows batch file
    with open(os.path.join(base_dir, "start_game.bat"), "w") as f:
        f.write("@echo off\n")
        f.write("python core/main.py\n")
        f.write("pause\n")
    
    # macOS/Linux shell script
    with open(os.path.join(base_dir, "start_game.sh"), "w") as f:
        f.write("#!/bin/bash\n")
        f.write("python3 core/main.py\n")
    
    # Make shell script executable
    os.chmod(os.path.join(base_dir, "start_game.sh"), 0o755)

def create_zip_package(base_dir, version="1.0.0"):
    """Create a ZIP package for Windows."""
    package_name = f"code-of-pride-windows-{version}.zip"
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arc_path)
    print(f"Created Windows package: {package_name}")

def create_tar_package(base_dir, version="1.0.0"):
    """Create a TAR package for macOS/Linux."""
    package_name = f"code-of-pride-unix-{version}.tar.gz"
    with tarfile.open(package_name, "w:gz") as tar:
        tar.add(base_dir, arcname=os.path.basename(base_dir))
    print(f"Created Unix package: {package_name}")

def create_installer_script():
    """Create a simple installer script."""
    installer_content = """#!/bin/bash
# Code of Pride Installer Script

echo "Installing Code of Pride..."

# Create virtual environment
python3 -m venv code-of-pride-env
source code-of-pride-env/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Installation complete!"
echo "To run the game, execute: python core/main.py"
"""
    
    with open("install.sh", "w") as f:
        f.write(installer_content)
    
    os.chmod("install.sh", 0o755)
    print("Created installer script: install.sh")

def main():
    """Main function to create distributable packages."""
    print("Creating distributable packages for Code of Pride...")
    
    # Create directory structure
    print("Creating directory structure...")
    base_dir = create_directory_structure()
    
    # Copy files
    print("Copying files...")
    copy_files(base_dir)
    
    # Create startup scripts
    print("Creating startup scripts...")
    create_startup_scripts(base_dir)
    
    # Get version from config or default
    version = "1.0.0"
    try:
        import config
        version = getattr(config, "VERSION", "1.0.0")
    except ImportError:
        pass
    
    # Create packages
    print("Creating ZIP package...")
    create_zip_package(base_dir, version)
    
    print("Creating TAR package...")
    create_tar_package(base_dir, version)
    
    # Create installer
    print("Creating installer script...")
    create_installer_script()
    
    # Cleanup
    print("Cleaning up...")
    shutil.rmtree(base_dir)
    
    print("Package creation complete!")
    print(f"Packages created:")
    print(f"  - code-of-pride-windows-{version}.zip")
    print(f"  - code-of-pride-unix-{version}.tar.gz")
    print(f"  - install.sh")

if __name__ == "__main__":
    main()