import boto3

s3 = boto3.client("s3")

bucket="devops-demo-1b381580"
# Delete object then bucket
s3.delete_object(Bucket=bucket, Key="hello.txt")
s3.delete_bucket(Bucket=bucket)
