#!/usr/bin/env python3
"""
Example 9: Setting Timeouts
==========================

This example demonstrates how to set timeouts for HTTP requests.
Timeouts prevent your program from hanging indefinitely when a server is slow or unresponsive.

Types of timeouts:
- Connection timeout: How long to wait for a connection to be established
- Read timeout: How long to wait for the server to send data
- Total timeout: Maximum time for the entire request
"""

import requests
import time

# Base URL for httpbin.org
BASE_URL = "https://httpbin.org"

def timeout_example():
    """
    Demonstrate different timeout scenarios.
    """
    print("=== Setting Timeouts Example ===")
    print()

    # Example 1: Successful request with timeout
    print("1️⃣  Fast request with timeout:")
    try:
        start_time = time.time()
        # Set a timeout of 5 seconds for a request that should complete quickly
        response = requests.get(f"{BASE_URL}/delay/1", timeout=5)
        end_time = time.time()

        print(f"✅ Status Code: {response.status_code}")
        print(f"⏱️  Request took {end_time - start_time:.2f} seconds")
        print("   Request completed within timeout!")

    except requests.exceptions.Timeout:
        print("❌ The request timed out!")
    print()

    # Example 2: Timeout error
    print("2️⃣  Slow request that will timeout:")
    try:
        start_time = time.time()
        # Try to access an endpoint that takes 3 seconds, but set timeout to 2 seconds
        response = requests.get(f"{BASE_URL}/delay/3", timeout=2)
        end_time = time.time()

        print(f"✅ Status Code: {response.status_code}")
        print(f"⏱️  Request took {end_time - start_time:.2f} seconds")

    except requests.exceptions.Timeout as timeout_err:
        end_time = time.time()
        print(f"❌ Timeout error occurred after {end_time - start_time:.2f} seconds")
        print("   The server took too long to respond")
    print()

    # Example 3: Different timeout configurations
    print("3️⃣  Different timeout configurations:")
    print("   timeout=5           -> 5 seconds total timeout")
    print("   timeout=(3, 7)      -> 3s connect timeout, 7s read timeout")
    print("   timeout=None        -> No timeout (not recommended!)")
    print()

    print("💡 Timeout Best Practices:")
    print("- Always set reasonable timeouts for production code")
    print("- Use shorter timeouts for user-facing applications")
    print("- Consider using (connect_timeout, read_timeout) tuple for fine control")
    print("- Handle timeout exceptions gracefully")
    print("- Test with different timeout values to find the right balance")

    print()

def main():
    """
    Run the timeout example.
    """
    print("Requests Library - Example 9: Setting Timeouts")
    print("=" * 50)
    print()

    timeout_example()

    print("🎉 Example completed! Timeouts keep your applications responsive.")

if __name__ == "__main__":
    main()