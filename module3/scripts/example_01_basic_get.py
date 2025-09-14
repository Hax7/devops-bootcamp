#!/usr/bin/env python3
"""
Example 1: Basic GET Request
============================

This example demonstrates how to make a simple GET request using the requests library.
A GET request retrieves data from a server.

First, install the requests library if you haven't already:
    pip install requests
"""

import requests

# Base URL for httpbin.org (a free service for testing HTTP requests)
BASE_URL = "https://httpbin.org"

def basic_get_request():
    """
    Make a basic GET request to retrieve data from the server.
    """
    print("=== Basic GET Request Example ===")
    print()

    # Make a simple GET request
    response = requests.get(f"{BASE_URL}/get")

    # Check if the request was successful (status code 200 means success)
    if response.status_code == 200:
        print(f"✅ Status Code: {response.status_code} (Success!)")
        print()
        print("📄 Response JSON:")
        print(response.json())
        print()
        print("💡 What happened:")
        print("- We sent a GET request to https://httpbin.org/get")
        print("- The server responded with status code 200 (OK)")
        print("- The response contains information about our request")
        print("- httpbin.org echoes back details about the request we made")
    else:
        print(f"❌ Error: Status Code {response.status_code}")
        print("The request was not successful")

    print()

def main():
    """
    Run the basic GET request example.
    """
    print("Requests Library - Example 1: Basic GET Request")
    print("=" * 50)
    print()

    basic_get_request()

    print("🎉 Example completed! Try running this with different URLs.")

if __name__ == "__main__":
    main()