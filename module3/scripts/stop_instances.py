import boto3

ec2 = boto3.client("ec2")

ec2.stop_instances(InstanceIds=["i-04c0fbb8e38b291a7","i-0b576eafa2c0df3fa","i-0fea54f9ad749d860"])