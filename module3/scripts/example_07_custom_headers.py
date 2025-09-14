#!/usr/bin/env python3
"""
Example 7: Custom Headers
========================

This example shows how to send custom headers with your HTTP requests.
Headers provide additional information about the request to the server.

Common headers include:
- User-Agent: Identifies your application
- Authorization: For authentication (API keys, tokens)
- Content-Type: Specifies the format of the request body
- Accept: Specifies what response formats you can handle
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def handling_headers():
    """
    Make a request with custom headers.
    """
    print("=== Custom Headers Example ===")
    print()

    # Custom headers to send with the request
    headers = {
        'User-Agent': 'My Python App v1.0',
        'Authorization': 'Bearer your-token-here',
        'Content-Type': 'application/json',
        'X-Custom-Header': 'My Custom Value'
    }

    print("📤 Sending custom headers:")
    for key, value in headers.items():
        print(f"   {key}: {value}")
    print()

    # Make request with custom headers
    response = requests.get(f"{BASE_URL}/headers", headers=headers)

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent custom headers with our request")
    print("- The server received all our headers and echoed them back")
    print("- Headers are key-value pairs that provide metadata about the request")
    print("- Common headers include User-Agent, Authorization, Content-Type")
    print("- Custom headers (starting with X-) can be used for your own purposes")
    print("- Headers help servers understand how to process your request")

    print()

def main():
    """
    Run the custom headers example.
    """
    print("Requests Library - Example 7: Custom Headers")
    print("=" * 50)
    print()

    handling_headers()

    print("🎉 Example completed! Headers are essential for API authentication and metadata.")

if __name__ == "__main__":
    main()