import boto3
from botocore.exceptions import ClientError


def resolve_latest_ami_id(region_name: str | None = None) -> str:
  """
  Resolve the latest Amazon Linux AMI ID for the current region.

  Preference order:
  1) Amazon Linux 2023 (x86_64) via SSM Parameter Store
  2) Amazon Linux 2 (x86_64) via SSM Parameter Store
  3) Fallback to EC2 DescribeImages (sorted by CreationDate)
  """
  session = boto3.session.Session(region_name=region_name)
  ssm = session.client("ssm")
  ec2 = session.client("ec2")

  ssm_params = [
    "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64",
    "/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2",
  ]

  # Try public SSM parameters first (fast, maintained by AWS)
  for name in ssm_params:
    try:
      param = ssm.get_parameter(Name=name)
      ami_id = param["Parameter"]["Value"].strip()
      if ami_id:
        print(ami_id)
        return ami_id
    except ClientError as e:
      # Continue to next option or fallback
      print(f"SSM parameter {name} not found: {e}")
      pass

  # Fallback: query EC2 images owned by Amazon and pick the newest
  try:
    images = ec2.describe_images(
      Owners=["amazon"],
      Filters=[
        {"Name": "name", "Values": [
          "al2023-ami-minimal-2023.*-x86_64",
          "amzn2-ami-hvm-*-x86_64-gp2",
        ]},
        {"Name": "architecture", "Values": ["x86_64"]},
        {"Name": "state", "Values": ["available"]},
        {"Name": "root-device-type", "Values": ["ebs"]},
        {"Name": "virtualization-type", "Values": ["hvm"]},
      ],
    )["Images"]
    if not images:
      raise RuntimeError("No matching Amazon Linux images found.")
    images.sort(key=lambda i: i["CreationDate"], reverse=True)
    return images[0]["ImageId"]
  except ClientError as e:
    raise RuntimeError(f"Failed to resolve latest AMI: {e}")


def main():
  session = boto3.session.Session()
  region = session.region_name or "us-east-1"  # fallback if not configured
  ec2 = session.client("ec2", region_name=region)

  image_id = resolve_latest_ami_id(region)
  instance_type = "t3.micro"  # current generation burstable (x86_64)

  print(f"Launching EC2 in {region} with AMI {image_id} and type {instance_type}...")

  response = ec2.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
      {
        "ResourceType": "instance",
        "Tags": [{"Key": "Name", "Value": "ahmad-ec2"}],
      }
    ],
  )
  instance_id = response["Instances"][0]["InstanceId"]
  print("Launched:", instance_id)


if __name__ == "__main__":
  main()
