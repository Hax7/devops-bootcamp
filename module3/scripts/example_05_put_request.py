#!/usr/bin/env python3
"""
Example 5: PUT Request
=====================

This example demonstrates how to make a PUT request to update existing resources.
PUT requests are used to completely replace or update a resource on the server.

PUT is similar to POST but is used for updates rather than creating new resources.
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def put_request():
    """
    Make a PUT request to update a resource.
    """
    print("=== PUT Request Example ===")
    print()

    # Updated data to send
    updated_data = {
        'name': 'Updated Name',
        'status': 'active',
        'last_modified': '2025-09-13'
    }

    print("📤 Sending updated data:")
    for key, value in updated_data.items():
        print(f"   {key}: {value}")
    print()

    # Make PUT request
    response = requests.put(f"{BASE_URL}/put", json=updated_data)

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent a PUT request to update a resource")
    print("- PUT requests are used to replace/update existing data")
    print("- The server received our data and echoed it back")
    print("- In a real API, this would update an existing record")
    print("- PUT typically replaces the entire resource (vs PATCH which partially updates)")

    print()

def main():
    """
    Run the PUT request example.
    """
    print("Requests Library - Example 5: PUT Request")
    print("=" * 50)
    print()

    put_request()

    print("🎉 Example completed! PUT requests are for updating existing resources.")

if __name__ == "__main__":
    main()