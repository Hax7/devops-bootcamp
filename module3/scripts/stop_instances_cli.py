import argparse
from typing import Iterable, List, Optional

import boto3
from botocore.exceptions import ClientError


def _flatten_instance_ids(reservations: Iterable[dict]) -> List[str]:
    ids: List[str] = []
    for r in reservations:
        for i in r.get("Instances", []):
            ids.append(i["InstanceId"])
    return ids


def find_instances(ec2, ids: Optional[List[str]], name: Optional[str]) -> List[str]:
    if ids:
        try:
            resp = ec2.describe_instances(InstanceIds=ids)
        except ClientError as e:
            raise SystemExit(f"Failed to describe instances by ids: {e}")
        # filter to running only for stopping
        running = []
        for r in resp.get("Reservations", []):
            for inst in r.get("Instances", []):
                if inst.get("State", {}).get("Name") == "running":
                    running.append(inst["InstanceId"])
        return running

    filters = [
        {"Name": "instance-state-name", "Values": ["running"]},
    ]
    if name:
        filters.append({"Name": "tag:Name", "Values": [name]})

    try:
        paginator = ec2.get_paginator("describe_instances")
        pages = paginator.paginate(Filters=filters)
        reservations: List[dict] = []
        for page in pages:
            reservations.extend(page.get("Reservations", []))
        return _flatten_instance_ids(reservations)
    except ClientError as e:
        raise SystemExit(f"Failed to find running instances: {e}")


def main():
    parser = argparse.ArgumentParser(description="Stop EC2 instances by ID or Name tag")
    parser.add_argument(
        "--ids",
        nargs="+",
        help="One or more EC2 instance IDs to stop",
    )
    parser.add_argument(
        "--name",
        default="demo-ec2",
        help="Value of the Name tag to match (default: demo-ec2)",
    )
    parser.add_argument(
        "--region",
        help="AWS region (defaults to current configured region)",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait until instances reach stopped state",
    )
    args = parser.parse_args()

    session = boto3.session.Session(region_name=args.region)
    region = session.region_name or "us-east-1"
    ec2 = session.client("ec2", region_name=region)

    target_ids = find_instances(ec2, ids=args.ids, name=args.name)
    if not target_ids:
        print("No running instances matched the criteria.")
        return

    print(f"Stopping {len(target_ids)} instance(s) in {region}: {', '.join(target_ids)}")
    try:
        ec2.stop_instances(InstanceIds=target_ids)
    except ClientError as e:
        raise SystemExit(f"Failed to stop instances: {e}")

    if args.wait:
        print("Waiting for instances to stop...")
        waiter = ec2.get_waiter("instance_stopped")
        waiter.wait(InstanceIds=target_ids)
        print("All instances stopped.")


if __name__ == "__main__":
    main()
