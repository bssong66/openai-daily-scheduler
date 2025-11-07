#!/usr/bin/env python3
import os
import requests
import sys
from datetime import datetime

# Get environment variables
api_key = os.getenv('OPENAI_API_KEY')
workflow_id = os.getenv('WORKFLOW_ID')

if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

if not workflow_id:
    print("Error: WORKFLOW_ID environment variable not set")
    sys.exit(1)

# OpenAI API endpoint for running a workflow
url = f"https://api.openai.com/v1/workflows/{workflow_id}/runs"

# Headers with authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    print(f"[{datetime.now().isoformat()}] Starting OpenAI workflow execution...")
    print(f"Workflow ID: {workflow_id}")
    
    # Make the API request
    response = requests.post(url, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"[{datetime.now().isoformat()}] Workflow started successfully!")
        print(f"Response: {response.json()}")
        sys.exit(0)
    else:
        print(f"[{datetime.now().isoformat()}] Error: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"[{datetime.now().isoformat()}] Exception occurred: {str(e)}")
    sys.exit(1)
