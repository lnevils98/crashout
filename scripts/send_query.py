#!/usr/bin/env python3
"""
Simple script to POST a JSON prompt to the FastAPI /query endpoint and print the response.

Usage:
  python scripts/send_query.py
  python scripts/send_query.py --url http://127.0.0.1:8000/query --role user --content "Hello"
"""

import argparse
import json
import sys

import requests


def main():
    parser = argparse.ArgumentParser(description="Send a JSON prompt to /query and print the response")
    parser.add_argument("--url", default="http://127.0.0.1:8000/query", help="Full URL of the /query endpoint")
    parser.add_argument("--role", default="user", help="role field for the prompt")
    parser.add_argument("--content", default="How long is a marathon?", help="content field for the prompt")
    parser.add_argument("--timeout", type=float, default=60.0, help="request timeout in seconds")

    args = parser.parse_args()

    payload = {"role": args.role, "content": args.content}

    try:
        resp = requests.post(args.url, json=payload, timeout=args.timeout)
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"HTTP {resp.status_code}\n")

    # Try to pretty-print JSON responses, otherwise print raw text
    try:
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except ValueError:
        print(resp.text)

    # Exit non-zero on server errors
    if resp.status_code >= 500:
        sys.exit(1)


if __name__ == "__main__":
    main()
