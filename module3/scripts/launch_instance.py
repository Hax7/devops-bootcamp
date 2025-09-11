import boto3

ec2 = boto3.client("ec2")

response = ec2.run_instances(
    ImageId="ami-00ca32bbc84273381",  # choose a valid AMI in your region
    InstanceType="t3.micro",
    MinCount=1, MaxCount=1,
    TagSpecifications=[{
      "ResourceType": "instance",
      "Tags": [{"Key": "Name", "Value": "demo-ec2"}]
    }]
)
instance_id = response["Instances"][0]["InstanceId"]
print("Launched:", instance_id)
