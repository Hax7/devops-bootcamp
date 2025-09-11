import boto3
from pprint import pprint

s3 = boto3.client("s3")
resp = s3.list_buckets()
pprint([b["Name"] for b in resp.get("Buckets", [])])
