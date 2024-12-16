import os
import shutil
from pathlib import Path

def find_files_to_delete(root_dir):
    # Patterns to match for deletion
    temp_patterns = ['.tmp', '.temp', '.log', '.DS_Store', 'Thumbs.db']
    build_dirs = ['dist', 'build', '__pycache__', '.cache', 'node_modules']
    ide_dirs = ['.idea', '.vscode']
    backup_patterns = ['_backup', '_old', '_archive', '.bak']
    
    files_to_delete = []
    dirs_to_delete = []

    for root, dirs, files in os.walk(root_dir):
        # Check directories
        for dir_name in dirs:
            full_dir_path = os.path.join(root, dir_name)
            if dir_name in build_dirs or dir_name in ide_dirs:
                dirs_to_delete.append(full_dir_path)

        # Check files
        for file_name in files:
            full_file_path = os.path.join(root, file_name)
            
            # Check temporary files
            if any(pattern in file_name for pattern in temp_patterns):
                files_to_delete.append(full_file_path)
            
            # Check backup files
            if any(pattern in file_name for pattern in backup_patterns):
                files_to_delete.append(full_file_path)

    return files_to_delete, dirs_to_delete

def print_deletion_candidates(files, dirs):
    print("\nFiles marked for deletion:")
    for file in files:
        print(f"- {file}")
    
    print("\nDirectories marked for deletion:")
    for dir_path in dirs:
        print(f"- {dir_path}")

def confirm_deletion():
    return input("\nDo you want to proceed with deletion? (yes/no): ").lower() == 'yes'

def delete_files_and_dirs(files, dirs):
    # Delete files first
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    # Delete directories
    for dir_path in dirs:
        try:
            shutil.rmtree(dir_path)
            print(f"Deleted directory: {dir_path}")
        except Exception as e:
            print(f"Error deleting {dir_path}: {e}")

def main():
    root_dir = "."  # Current directory, modify as needed
    files_to_delete, dirs_to_delete = find_files_to_delete(root_dir)
    
    print_deletion_candidates(files_to_delete, dirs_to_delete)
    
    if confirm_deletion():
        delete_files_and_dirs(files_to_delete, dirs_to_delete)
        print("\nCleanup completed!")
    else:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()