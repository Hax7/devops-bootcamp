import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client("ec2")
vpcs = ec2.describe_vpcs()["Vpcs"]
default_vpc = [v["VpcId"] for v in vpcs if v.get("IsDefault")][0]

group_name = "demo-sg"

# Create the security group or reuse if it already exists
try:
    sg = ec2.create_security_group(
        GroupName=group_name,
        Description="Demo Security Group",
        VpcId=default_vpc,
    )
    sg_id = sg["GroupId"]
    print("Created SG:", sg_id)
except ClientError as e:
    code = e.response.get("Error", {}).get("Code")
    if code in {"InvalidGroup.Duplicate", "Resource.AlreadyExists"}:
        # Look up existing SG by name in the same VPC
        resp = ec2.describe_security_groups(
            Filters=[
                {"Name": "group-name", "Values": [group_name]},
                {"Name": "vpc-id", "Values": [default_vpc]},
            ]
        )
        sgs = resp.get("SecurityGroups", [])
        if not sgs:
            raise
        sg_id = sgs[0]["GroupId"]
        print("Using existing SG:", sg_id)
    else:
        raise

# Authorize inbound SSH (TCP 22) from anywhere.
# Note: For production, restrict the CIDR to your IP range.
try:
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [
                    {"CidrIp": "0.0.0.0/0", "Description": "SSH from anywhere (IPv4)"}
                ],
                "Ipv6Ranges": [
                    {"CidrIpv6": "::/0", "Description": "SSH from anywhere (IPv6)"}
                ],
            }
        ],
    )
    print("Added SSH ingress on tcp/22")
except ClientError as e:
    # Ignore duplicate rule errors to keep the script idempotent-ish
    code = e.response.get("Error", {}).get("Code")
    if code in {"InvalidPermission.Duplicate", "InvalidPermission.DuplicatePermission"}:
        print("SSH ingress already exists")
    else:
        raise
desc = ec2.describe_security_groups(GroupIds=[sg_id])
print("Current rules:", desc["SecurityGroups"][0]["IpPermissions"])

ec2.delete_security_group(GroupId=sg_id)