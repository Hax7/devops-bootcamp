#!/usr/bin/env python3

import os
from fabric import Connection

# Function to update nginx default page
def update_nginx_page(host):
    try:
        with Connection(host=host, user='ubuntu') as conn:
            # Check if the file exists
            result = conn.run('ls /var/www/html/index.nginx-debian.html', hide=True)
            if result.ok:
                # Update the welcome message
                conn.sudo('sed -i "s/Welcome to nginx!/Welcome to DevOps Bootcamp!/g" /var/www/html/index.nginx-debian.html')
                print(f"Updated nginx page on {host}")
            else:
                print(f"Nginx default page not found on {host}")
    except Exception as e:
        print(f"Failed to update {host}: {e}")

def main():
    # Read IPs from file
    ips_file = 'instance_ips.txt'
    if not os.path.exists(ips_file):
        print(f"IPs file {ips_file} not found. Please run the launch script first.")
        return

    with open(ips_file, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    if not ips:
        print("No IPs found in the file.")
        return

    print(f"Updating nginx on {len(ips)} instances...")

    # Iterate over each IP and update
    for ip in ips:
        update_nginx_page(ip)

    print("All updates completed.")

if __name__ == "__main__":
    main()