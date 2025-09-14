#!/usr/bin/env python3
"""
Example 4: POST Request with Form Data
=====================================

This example shows how to send form data using a POST request.
Form data is commonly used when submitting web forms.

Unlike JSON, form data is sent as key-value pairs in the request body.
"""

import requests

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def post_with_form_data():
    """
    Make a POST request with form data.
    """
    print("=== POST Request with Form Data ===")
    print()

    # Form data to send (like a web form submission)
    form_data = {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'message': 'Hello from Python!'
    }

    print("📤 Sending form data:")
    for key, value in form_data.items():
        print(f"   {key}: {value}")
    print()

    # Make POST request with form data
    # Note: we use 'data' parameter instead of 'json'
    response = requests.post(f"{BASE_URL}/post", data=form_data)

    print(f"✅ Status Code: {response.status_code}")
    print()
    print("📄 Response JSON:")
    response_data = response.json()
    print(response_data)
    print()
    print("💡 What happened:")
    print("- We sent form data using the 'data' parameter")
    print("- The data was URL-encoded (spaces become +, special chars encoded)")
    print("- Content-Type was automatically set to 'application/x-www-form-urlencoded'")
    print("- Our data appears in the 'form' field of the response")
    print("- Compare this with the JSON example - the data structure is different!")

    print()

def main():
    """
    Run the POST with form data example.
    """
    print("Requests Library - Example 4: POST with Form Data")
    print("=" * 50)
    print()

    post_with_form_data()

    print("🎉 Example completed! Form data is perfect for web form submissions.")

if __name__ == "__main__":
    main()