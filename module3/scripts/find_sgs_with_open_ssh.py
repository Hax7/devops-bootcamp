# Find SGs exposing SSH to the world
import boto3

ec2 = boto3.client("ec2")
sgs = ec2.describe_security_groups()["SecurityGroups"]
risky = []
for g in sgs:
    for p in g.get("IpPermissions", []):
        for r in p.get("IpRanges", []):
            if r.get("CidrIp") == "0.0.0.0/0" and p.get("FromPort") in (22, 3389):
                risky.append(g["GroupId"])
print("Risky SGs:", risky)
