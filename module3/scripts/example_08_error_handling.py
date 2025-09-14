#!/usr/bin/env python3
"""
Example 8: Error Handling
========================

This example demonstrates proper error handling for HTTP requests.
Network requests can fail for many reasons, so it's important to handle errors gracefully.

Common types of errors:
- HTTP errors (4xx, 5xx status codes)
- Connection errors (network issues)
- Timeout errors (server too slow)
- Other request exceptions
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def error_handling():
    """
    Demonstrate different types of error handling.
    """
    print("=== Error Handling Example ===")
    print()

    # Example 1: HTTP Error (404 Not Found)
    print("1️⃣  Testing HTTP Error (404):")
    try:
        # Try to access a non-existent endpoint
        response = requests.get(f"{BASE_URL}/nonexistent")

        # This will raise an exception for HTTP error status codes
        response.raise_for_status()

        print("✅ Request successful!")
        print(response.json())

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
        print("   This means the server returned an error status code (4xx or 5xx)")
    print()

    # Example 2: Connection Error
    print("2️⃣  Testing Connection Error:")
    try:
        # Try to connect to a non-existent domain
        response = requests.get("https://this-domain-does-not-exist-12345.com")

        response.raise_for_status()
        print("✅ Request successful!")

    except requests.exceptions.ConnectionError as conn_err:
        print(f"❌ Connection error occurred: {conn_err}")
        print("   This means we couldn't connect to the server")
    print()

    # Example 3: Timeout Error
    print("3️⃣  Testing Timeout Error:")
    try:
        # Try to access an endpoint that takes too long
        response = requests.get(f"{BASE_URL}/delay/10", timeout=3)

        response.raise_for_status()
        print("✅ Request completed successfully!")

    except requests.exceptions.Timeout as timeout_err:
        print(f"❌ Timeout error occurred: {timeout_err}")
        print("   This means the server took too long to respond")
    print()

    print("💡 Error Handling Best Practices:")
    print("- Always wrap requests in try-except blocks")
    print("- Use response.raise_for_status() to check for HTTP errors")
    print("- Handle specific exception types for different error scenarios")
    print("- Provide meaningful error messages to users")
    print("- Consider retry logic for transient errors")

    print()

def main():
    """
    Run the error handling example.
    """
    print("Requests Library - Example 8: Error Handling")
    print("=" * 50)
    print()

    error_handling()

    print("🎉 Example completed! Proper error handling makes your code robust.")

if __name__ == "__main__":
    main()