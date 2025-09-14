#!/usr/bin/env python3
"""
Test Script for S3 File Monitor
==============================

This script creates some test files to demonstrate the S3 file monitor functionality.
Run this in a separate terminal while the monitor is running.

Usage:
    python test_s3_monitor.py [test_folder]

If no test_folder is provided, it will create files in './test_files'
"""

import os
import sys
import time
from pathlib import Path

def create_test_files(test_folder):
    """
    Create various test files to demonstrate the monitor.

    Args:
        test_folder: Folder where test files will be created
    """
    print(f"📁 Creating test files in: {test_folder}")

    # Create test folder if it doesn't exist
    Path(test_folder).mkdir(parents=True, exist_ok=True)

    # Test files with different content types
    test_files = [
        ("hello.txt", "Hello, World!\nThis is a test file for S3 upload."),
        ("data.json", '{"name": "test", "value": 123, "active": true}'),
        ("config.yaml", "app:\n  name: test-app\n  version: 1.0\n  debug: true"),
        ("script.py", "#!/usr/bin/env python3\nprint('Hello from S3!')"),
        ("readme.md", "# Test File\n\nThis file was uploaded to S3 automatically!")
    ]

    created_files = []

    for filename, content in test_files:
        file_path = os.path.join(test_folder, filename)

        # Create the file
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"✅ Created: {filename}")
        created_files.append(file_path)

    return created_files

def modify_test_files(test_files):
    """
    Modify existing test files to trigger modification events.

    Args:
        test_files: List of file paths to modify
    """
    print("\n🔄 Modifying test files...")

    for file_path in test_files:
        time.sleep(1)  # Small delay between modifications

        filename = os.path.basename(file_path)

        if filename.endswith('.txt'):
            # Append to text file
            with open(file_path, 'a') as f:
                f.write(f"\n\nUpdated at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📝 Modified: {filename}")

        elif filename.endswith('.json'):
            # Update JSON content
            new_content = f'{{"name": "test", "value": {int(time.time())}, "active": true, "updated": true}}'
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"📝 Modified: {filename}")

        elif filename.endswith('.md'):
            # Update markdown
            with open(file_path, 'a') as f:
                f.write(f"\n\n## Update\nFile modified at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📝 Modified: {filename}")

def main():
    """
    Main test function.
    """
    print("🧪 S3 File Monitor Test Script")
    print("=" * 40)

    # Determine test folder
    test_folder = sys.argv[1] if len(sys.argv) > 1 else "./test_files"

    print(f"Test folder: {os.path.abspath(test_folder)}")
    print()

    # Create test files
    test_files = create_test_files(test_folder)

    # Wait a bit
    print("\n⏳ Waiting 3 seconds before modifications...")
    time.sleep(3)

    # Modify files
    modify_test_files(test_files)

    print("\n✅ Test completed!")
    print("Check your S3 bucket and the monitor logs for uploaded files.")
    print(f"Test files created in: {os.path.abspath(test_folder)}")

if __name__ == "__main__":
    main()