#!/usr/bin/env python3
"""
Example 6: DELETE Request
========================

This example demonstrates how to make a DELETE request to remove a resource
from the server. DELETE requests are used to delete existing resources.
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def delete_request():
    """
    Make a DELETE request to remove a resource.
    """
    print("=== DELETE Request Example ===")
    print()

    print("🗑️  Attempting to delete a resource...")
    print()

    # Make DELETE request
    response = requests.delete(f"{BASE_URL}/delete")

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent a DELETE request to remove a resource")
    print("- DELETE requests are used to delete existing data")
    print("- The server received our request and echoed back the details")
    print("- In a real API, this would delete a record from the database")
    print("- DELETE requests typically don't need a request body")
    print("- The response confirms the request was received and processed")

    print()

def main():
    """
    Run the DELETE request example.
    """
    print("Requests Library - Example 6: DELETE Request")
    print("=" * 50)
    print()

    delete_request()

    print("🎉 Example completed! DELETE requests are for removing resources.")

if __name__ == "__main__":
    main()