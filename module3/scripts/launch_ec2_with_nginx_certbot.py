import sys
from typing import Optional

import boto3
from botocore.exceptions import ClientError


CANONICAL_OWNER_ID = "099720109477"  # Ubuntu (Canonical)


def resolve_latest_ubuntu_ami(region_name: Optional[str] = None) -> str:
    """Resolve the latest Ubuntu LTS (22.04 or 24.04) AMD64 AMI ID for the region.

    Strategy: query Canonical-owned images for jammy (22.04) and noble (24.04),
    then pick the newest by CreationDate.
    """
    session = boto3.session.Session(region_name=region_name)
    ec2 = session.client("ec2")

    name_filters = [
        "ubuntu/images/hvm-ssd/ubuntu-noble-24.04-amd64-server-*",
        "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*",
    ]

    try:
        images = ec2.describe_images(
            Owners=[CANONICAL_OWNER_ID],
            Filters=[
                {"Name": "name", "Values": name_filters},
                {"Name": "architecture", "Values": ["x86_64"]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "root-device-type", "Values": ["ebs"]},
                {"Name": "virtualization-type", "Values": ["hvm"]},
            ],
        )["Images"]
        if not images:
            raise RuntimeError("No matching Ubuntu images found from Canonical.")
        images.sort(key=lambda i: i["CreationDate"], reverse=True)
        return images[0]["ImageId"]
    except ClientError as e:
        raise RuntimeError(f"Failed to resolve latest Ubuntu AMI: {e}")


def get_default_vpc_id(ec2):
    vpcs = ec2.describe_vpcs()["Vpcs"]
    for v in vpcs:
        if v.get("IsDefault"):
            return v["VpcId"]
    raise RuntimeError("No default VPC found in this account/region.")


def get_default_subnet_id(ec2, vpc_id: str) -> str:
    # Prefer subnets in the default VPC that are default for their AZs
    subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])["Subnets"]
    default_subnets = [s for s in subnets if s.get("DefaultForAz")]
    chosen = (default_subnets or subnets)
    if not chosen:
        raise RuntimeError("No subnets found in the default VPC.")
    # Pick the first deterministically (sorted by SubnetId)
    chosen.sort(key=lambda s: s["SubnetId"])
    return chosen[0]["SubnetId"]


def ensure_web_sg(ec2, vpc_id: str, group_name: str = "web-http-https-sg") -> str:
    # Create the security group or reuse if it already exists in the VPC
    try:
        resp = ec2.create_security_group(
            GroupName=group_name,
            Description="Allow HTTP/HTTPS",
            VpcId=vpc_id,
        )
        sg_id = resp["GroupId"]
        # Tag for convenience
        ec2.create_tags(Resources=[sg_id], Tags=[{"Key": "Name", "Value": group_name}])
        created = True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        if code in {"InvalidGroup.Duplicate", "Resource.AlreadyExists"}:
            # Look up existing SG by name in the same VPC
            desc = ec2.describe_security_groups(
                Filters=[
                    {"Name": "group-name", "Values": [group_name]},
                    {"Name": "vpc-id", "Values": [vpc_id]},
                ]
            )
            sgs = desc.get("SecurityGroups", [])
            if not sgs:
                raise
            sg_id = sgs[0]["GroupId"]
            created = False
        else:
            raise

    # Ensure HTTP (80) and HTTPS (443) rules exist (idempotent)
    for from_to in [(80, 80), (443, 443)]:
        try:
            ec2.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        "IpProtocol": "tcp",
                        "FromPort": from_to[0],
                        "ToPort": from_to[1],
                        "IpRanges": [
                            {"CidrIp": "0.0.0.0/0", "Description": "IPv4 anywhere"}
                        ],
                        "Ipv6Ranges": [
                            {"CidrIpv6": "::/0", "Description": "IPv6 anywhere"}
                        ],
                    }
                ],
            )
        except ClientError as e:
            code = e.response.get("Error", {}).get("Code")
            if code in {"InvalidPermission.Duplicate", "InvalidPermission.DuplicatePermission"}:
                pass
            else:
                raise

    action = "Created" if created else "Using existing"
    print(f"{action} SG: {sg_id}")
    return sg_id


def build_user_data_script() -> str:
    # Cloud-init script to install nginx and certbot
    script = r"""#cloud-config
package_update: true
package_upgrade: true
runcmd:
  - apt-get update -y
  - apt-get install -y nginx snapd
  - systemctl enable --now nginx
  - snap install core; snap refresh core
  - snap install --classic certbot
  - ln -sf /snap/bin/certbot /usr/bin/certbot
  # Optionally, you can automatically obtain a certificate later via:
  # certbot --nginx -d yourdomain.com -d www.yourdomain.com --non-interactive --agree-tos -m you@example.com
"""
    return script


def main():
    session = boto3.session.Session()
    region = session.region_name or "us-east-1"
    ec2 = session.client("ec2", region_name=region)

    print(f"Region: {region}")

    # Network + SG
    vpc_id = get_default_vpc_id(ec2)
    subnet_id = get_default_subnet_id(ec2, vpc_id)
    sg_id = ensure_web_sg(ec2, vpc_id)

    # AMI and instance config
    image_id = resolve_latest_ubuntu_ami(region)
    instance_type = "t3.micro"  # current-gen burstable (Free Tier eligible in some regions)
    user_data = build_user_data_script()

    print(f"Launching EC2 with AMI {image_id} and type {instance_type}...")

    try:
        run_resp = ec2.run_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            NetworkInterfaces=[
                {
                    "DeviceIndex": 0,
                    "SubnetId": subnet_id,
                    "AssociatePublicIpAddress": True,
                    "Groups": [sg_id],
                }
            ],
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {"Key": "Name", "Value": "web-nginx-certbot"},
                    ],
                }
            ],
            UserData=user_data,
        )
    except ClientError as e:
        print(f"Failed to launch instance: {e}")
        sys.exit(1)

    instance_id = run_resp["Instances"][0]["InstanceId"]
    print("Launched:", instance_id)

    # Wait for running state
    waiter = ec2.get_waiter("instance_running")
    print("Waiting for instance to be running...")
    waiter.wait(InstanceIds=[instance_id])

    # Fetch public IP
    desc = ec2.describe_instances(InstanceIds=[instance_id])
    inst = desc["Reservations"][0]["Instances"][0]
    public_ip = inst.get("PublicIpAddress")

    if not public_ip:
        # In rare cases public IP may not be immediately populated; quick retry
        import time

        for _ in range(6):
            time.sleep(5)
            desc = ec2.describe_instances(InstanceIds=[instance_id])
            inst = desc["Reservations"][0]["Instances"][0]
            public_ip = inst.get("PublicIpAddress")
            if public_ip:
                break

    if public_ip:
        print(f"Public IP: {public_ip}")
    else:
        print("Instance is running but PublicIpAddress not found. Check subnet settings.")


if __name__ == "__main__":
    main()
