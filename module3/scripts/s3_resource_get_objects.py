import boto3

s3 = boto3.resource('s3')

bucket = s3.Bucket('aws-sam-cli-managed-default-samclisourcebucket-hzwnckspd6vh')

for obj in bucket.objects.all():
    print(obj.key, obj.last_modified)
