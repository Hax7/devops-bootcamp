import boto3

ec2 = boto3.client("ec2")

resp = ec2.describe_instances(
    Filters=[
      {"Name": "instance-state-name", "Values": ["running"]},
      {"Name": "tag:Environment", "Values": ["Dev"]}
    ]
)
running_dev = [i["InstanceId"]
               for r in resp["Reservations"]
               for i in r["Instances"]]

print("Running instances:", running_dev)