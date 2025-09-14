#!/usr/bin/env python3
"""
Example 3: POST Request
======================

This example demonstrates how to make a POST request to send data to a server.
POST requests are commonly used to create new resources or submit form data.

The data is sent in the request body as JSON.
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def post_request():
    """
    Make a POST request with JSON data.
    """
    print("=== POST Request Example ===")
    print()

    # Data to send in the request body
    data = {
        'username': 'johndoe',
        'email': 'john@example.com',
        'password': 'secret123'
    }

    print("📤 Sending JSON data:")
    for key, value in data.items():
        print(f"   {key}: {value}")
    print()

    # Make POST request with JSON data
    response = requests.post(f"{BASE_URL}/post", json=data)

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent a POST request with JSON data in the body")
    print("- The 'json' parameter automatically converts our dict to JSON")
    print("- The server received our data and echoed it back")
    print("- Notice the 'Content-Type: application/json' header was set automatically")
    print("- Our data appears in the 'json' field of the response")

    print()

def main():
    """
    Run the POST request example.
    """
    print("Requests Library - Example 3: POST Request")
    print("=" * 50)
    print()

    post_request()

    print("🎉 Example completed! POST requests are great for creating new data.")

if __name__ == "__main__":
    main()