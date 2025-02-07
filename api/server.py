import os
import requests
import json
from flask import Flask, Response
from flask_cors import CORS
from werkzeug.wrappers import Response as WResponse

app = Flask(__name__)
CORS(app)  # Allow all domains

# Get your API key from an environment variable (set this in Vercel)
API_KEY = os.environ.get("API_KEY", "vV7yhrHeM5SseeQHn7f-ndckmR8l4h4J")
BASE_URL = "https://api.rbxstats.xyz/api"

def proxy_request(target_url):
    """Helper function to forward the request to the target URL."""
    try:
        api_response = requests.get(target_url)
        return api_response.content, api_response.status_code, api_response.headers.get("Content-Type", "application/json")
    except Exception as e:
        return f"Error fetching data: {str(e)}", 500, "text/plain"

@app.route("/api/offsets")
def offsets():
    target_url = f"{BASE_URL}/offsets?api={API_KEY}"
    body, status, content_type = proxy_request(target_url)
    return Response(body, status=status, content_type=content_type)

@app.route("/api/offsets/plain")
def offsets_plain():
    target_url = f"{BASE_URL}/offsets/plain?api={API_KEY}"
    body, status, content_type = proxy_request(target_url)
    return Response(body, status=status, content_type=content_type)

@app.route("/api/offsets/search/<name>")
def offsets_search(name):
    target_url = f"{BASE_URL}/offsets/search/{name}?api={API_KEY}"
    body, status, content_type = proxy_request(target_url)
    return Response(body, status=status, content_type=content_type)

# Vercel expects a top-level handler function for Python serverless functions.
def handler(request):
    response = WResponse.from_app(app, request.environ)
    return {
        "statusCode": response.status_code,
        "headers": dict(response.headers),
        "body": response.get_data(as_text=True)
    }
