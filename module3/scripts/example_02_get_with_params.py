#!/usr/bin/env python3
"""
Example 2: GET Request with Query Parameters
===========================================

This example shows how to send data to the server using query parameters
in the URL. Query parameters are added to the URL after a '?' character.

Example URL with parameters: https://httpbin.org/get?name=John&age=25
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def get_with_parameters():
    """
    Make a GET request with query parameters.
    """
    print("=== GET Request with Query Parameters ===")
    print()

    # Parameters to send (these will be added to the URL)
    params = {
        'name': 'John Doe',
        'age': 25,
        'city': 'New York'
    }

    print("📤 Sending parameters:")
    for key, value in params.items():
        print(f"   {key}: {value}")
    print()

    # Make GET request with parameters
    response = requests.get(f"{BASE_URL}/get", params=params)

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("🔗 Full URL with parameters:")
    print(response.url)
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent parameters as part of the URL")
    print("- The server received our parameters in the 'args' field")
    print("- Notice how the URL was automatically encoded")
    print("- Spaces became '+' and special characters were handled")

    print()

def main():
    """
    Run the GET with parameters example.
    """
    print("Requests Library - Example 2: GET with Parameters")
    print("=" * 50)
    print()

    get_with_parameters()

    print("🎉 Example completed! Try changing the parameters and see how the URL changes.")

if __name__ == "__main__":
    main()