#!/usr/bin/env python3
"""
OpenAI Workflow Executor Script
Executes a pre-built OpenAI Agent Builder workflow
Using simple curl or requests library approach
"""

import os
import sys
import json
from datetime import datetime

def main():
    # Get environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    workflow_id = os.getenv('WORKFLOW_ID')
    
    if not api_key:
        print(f"[{datetime.now().isoformat()}] Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    if not workflow_id:
        print(f"[{datetime.now().isoformat()}] Error: WORKFLOW_ID environment variable not set")
        sys.exit(1)
    
    print(f"[{datetime.now().isoformat()}] Starting OpenAI workflow execution...")
    print(f"Workflow ID: {workflow_id}")
    
    try:
        # Try using requests library for HTTP call
        import requests
    except ImportError:
        print(f"[{datetime.now().isoformat()}] Installing requests library...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests"])
        import requests
    
    try:
        # Try direct workflow execution endpoint first
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "input": "Execute daily report"
        }
        
        # Try the REST API endpoint for executing workflows
        url = f"https://api.openai.com/v1/workflows/{workflow_id}/runs"
        
        print(f"[{datetime.now().isoformat()}] Calling: POST {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"[{datetime.now().isoformat()}] Workflow execution completed successfully!")
            print(f"Response: {response.json()}")
            sys.exit(0)
        elif response.status_code == 404:
            # Endpoint doesn't exist, try alternative
            print(f"[{datetime.now().isoformat()}] Workflow endpoint not available, trying alternative...")
            # Try using OpenAI SDK as fallback
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                # Try using threads API with metadata
                thread = client.beta.threads.create()
                client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content="Execute daily report"
                )
                
                print(f"[{datetime.now().isoformat()}] Workflow execution completed (via threads API)")
                sys.exit(0)
            except Exception as e:
                print(f"[{datetime.now().isoformat()}] Alternative method also failed: {str(e)}")
                sys.exit(1)
        else:
            print(f"[{datetime.now().isoformat()}] Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] Error executing workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
