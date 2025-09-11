import uuid, boto3
s3 = boto3.client("s3")
bucket = f"devops-demo-{uuid.uuid4().hex[:8]}"
s3.create_bucket(
    Bucket=bucket,
    CreateBucketConfiguration={"LocationConstraint": "us-east-2"}
)
print("Bucket:", bucket)

print("Uploading hello.txt")
from pathlib import Path
Path("hello.txt").write_text("Hello, S3!")
s3.upload_file("hello.txt", bucket, "hello.txt")

print("Reading back")
# List objects
objs = s3.list_objects_v2(Bucket=bucket).get("Contents", [])
print([o["Key"] for o in objs])

print("Getting hello.txt")
# Read bytes
obj = s3.get_object(Bucket=bucket, Key="hello.txt")
print(obj["Body"].read().decode())
