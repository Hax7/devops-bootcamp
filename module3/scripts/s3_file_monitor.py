#!/usr/bin/env python3
"""
S3 File Sync Monitor
===================

This script uses the watchdog library to monitor a folder for file changes
and automatically uploads new or modified files to an AWS S3 bucket using boto3.

Features:
- Monitors folder for new files and file modifications
- Automatically uploads files to S3
- Handles different file types
- Includes error handling and logging
- Configurable S3 bucket and folder paths

Prerequisites:
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- Required packages: pip install watchdog boto3

Usage:
    python s3_file_monitor.py /path/to/watch /your-bucket-name [s3-prefix]

Example:
    python s3_file_monitor.py ./documents my-bucket uploads/
"""

import os
import sys
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('s3_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class S3FileHandler(FileSystemEventHandler):
    """
    Custom event handler for file system events that uploads files to S3.
    """

    def __init__(self, s3_client, bucket_name, s3_prefix=""):
        """
        Initialize the S3 file handler.

        Args:
            s3_client: Boto3 S3 client
            bucket_name: Name of the S3 bucket
            s3_prefix: Prefix/path in S3 bucket (optional)
        """
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix.rstrip('/') + '/' if s3_prefix else ""

        logger.info(f"S3 Handler initialized - Bucket: {bucket_name}, Prefix: {self.s3_prefix}")

    def on_created(self, event):
        """
        Called when a file is created.
        """
        if not event.is_directory:
            self._handle_file_event(event.src_path, "created")

    def on_modified(self, event):
        """
        Called when a file is modified.
        """
        if not event.is_directory:
            self._handle_file_event(event.src_path, "modified")

    def _handle_file_event(self, file_path, event_type):
        """
        Handle file creation or modification events.

        Args:
            file_path: Path to the file that triggered the event
            event_type: Type of event ("created" or "modified")
        """
        try:
            # Get file information
            file_path_obj = Path(file_path)
            file_name = file_path_obj.name
            file_size = file_path_obj.stat().st_size

            # Create S3 key (path in bucket)
            s3_key = self.s3_prefix + file_name

            logger.info(f"📁 File {event_type}: {file_name} ({file_size} bytes)")

            # Upload file to S3
            self._upload_to_s3(file_path, s3_key, file_name)

        except Exception as e:
            logger.error(f"❌ Error processing file {file_path}: {str(e)}")

    def _upload_to_s3(self, local_path, s3_key, file_name):
        """
        Upload a file to S3 bucket.

        Args:
            local_path: Local file path
            s3_key: S3 object key
            file_name: Original file name for logging
        """
        try:
            # Determine content type based on file extension
            content_type = self._get_content_type(local_path)

            # Upload the file
            with open(local_path, 'rb') as file_data:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    Body=file_data,
                    ContentType=content_type
                )

            # Get the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"

            logger.info(f"✅ Successfully uploaded {file_name} to S3")
            logger.info(f"🔗 S3 URL: {s3_url}")

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                logger.error(f"❌ Bucket '{self.bucket_name}' does not exist")
            elif error_code == 'AccessDenied':
                logger.error(f"❌ Access denied to bucket '{self.bucket_name}'")
            else:
                logger.error(f"❌ S3 upload error: {e}")
        except FileNotFoundError:
            logger.error(f"❌ File not found: {local_path}")
        except Exception as e:
            logger.error(f"❌ Unexpected error uploading {file_name}: {str(e)}")

    def _get_content_type(self, file_path):
        """
        Determine the content type based on file extension.

        Args:
            file_path: Path to the file

        Returns:
            str: MIME content type
        """
        extension = Path(file_path).suffix.lower()

        content_types = {
            '.txt': 'text/plain',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.zip': 'application/zip',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip'
        }

        return content_types.get(extension, 'application/octet-stream')

def create_s3_client():
    """
    Create and configure S3 client.

    Returns:
        boto3.client: Configured S3 client

    Raises:
        NoCredentialsError: If AWS credentials are not found
    """
    try:
        s3_client = boto3.client('s3')

        # Test the connection by listing buckets
        s3_client.head_bucket(Bucket=s3_client.list_buckets()['Buckets'][0]['Name'])
        logger.info("✅ AWS S3 connection successful")
        return s3_client

    except NoCredentialsError:
        logger.error("❌ AWS credentials not found!")
        logger.error("   Please configure AWS credentials using:")
        logger.error("   - AWS CLI: aws configure")
        logger.error("   - Environment variables: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        logger.error("   - IAM roles (if running on EC2)")
        raise
    except Exception as e:
        logger.error(f"❌ Failed to create S3 client: {str(e)}")
        raise

def validate_bucket(s3_client, bucket_name):
    """
    Validate that the S3 bucket exists and is accessible.

    Args:
        s3_client: Boto3 S3 client
        bucket_name: Name of the bucket to validate

    Returns:
        bool: True if bucket exists and is accessible
    """
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logger.info(f"✅ Bucket '{bucket_name}' exists and is accessible")
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            logger.error(f"❌ Bucket '{bucket_name}' does not exist")
        elif error_code == 'AccessDenied':
            logger.error(f"❌ Access denied to bucket '{bucket_name}'")
        else:
            logger.error(f"❌ Error accessing bucket: {e}")
        return False

def main():
    """
    Main function to set up file monitoring and S3 sync.
    """
    print("🚀 S3 File Sync Monitor")
    print("=" * 50)

    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python s3_file_monitor.py <watch_path> <bucket_name> [s3_prefix]")
        print()
        print("Arguments:")
        print("  watch_path  : Local folder path to monitor")
        print("  bucket_name : AWS S3 bucket name")
        print("  s3_prefix   : Optional S3 folder prefix (e.g., 'uploads/')")
        print()
        print("Example:")
        print("  python s3_file_monitor.py ./documents my-bucket uploads/")
        sys.exit(1)

    watch_path = sys.argv[1]
    bucket_name = sys.argv[2]
    s3_prefix = sys.argv[3] if len(sys.argv) > 3 else ""

    # Validate watch path
    if not os.path.exists(watch_path):
        logger.error(f"❌ Watch path does not exist: {watch_path}")
        sys.exit(1)

    if not os.path.isdir(watch_path):
        logger.error(f"❌ Watch path is not a directory: {watch_path}")
        sys.exit(1)

    logger.info(f"📂 Monitoring folder: {os.path.abspath(watch_path)}")
    logger.info(f"🪣 S3 Bucket: {bucket_name}")
    logger.info(f"📁 S3 Prefix: {s3_prefix or '(root)'}")

    try:
        # Create S3 client
        s3_client = create_s3_client()

        # Validate bucket
        if not validate_bucket(s3_client, bucket_name):
            sys.exit(1)

        # Create event handler
        event_handler = S3FileHandler(s3_client, bucket_name, s3_prefix)

        # Create observer
        observer = Observer()
        observer.schedule(event_handler, watch_path, recursive=True)

        # Start monitoring
        logger.info("🔍 Starting file monitoring... (Press Ctrl+C to stop)")
        print()
        print("Monitoring started! Try creating or modifying files in:")
        print(f"  {os.path.abspath(watch_path)}")
        print()
        print("Files will be automatically uploaded to S3.")
        print("Check s3_monitor.log for detailed logs.")
        print()

        observer.start()

        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Stopping file monitor...")
            observer.stop()
            observer.join()
            logger.info("✅ File monitor stopped")

    except NoCredentialsError:
        logger.error("❌ AWS credentials required. See error message above.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()