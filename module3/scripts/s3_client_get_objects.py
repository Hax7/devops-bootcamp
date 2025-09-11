import boto3

client = boto3.client('s3')

response = client.list_objects_v2(Bucket='aws-sam-cli-managed-default-samclisourcebucket-hzwnckspd6vh')

for content in response['Contents']:
    obj_dict = client.get_object(Bucket='aws-sam-cli-managed-default-samclisourcebucket-hzwnckspd6vh', Key=content['Key'])
    print(content['Key'], obj_dict['LastModified'])
