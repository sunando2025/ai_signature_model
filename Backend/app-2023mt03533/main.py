from fastapi import FastAPI
import os
from pydantic import BaseModel

# Define a Pydantic model for the response
class AppInfo(BaseModel):
    app_version: str
    app_title: str

# Create FastAPI app instance
app = FastAPI()

# /get_info endpoint
@app.get("/get_info", response_model=AppInfo)
async def get_info():
    # Fetch environment variables
    app_version = os.getenv("APP_VERSION", "1.0")  # Default value "1.0"
    app_title = os.getenv("APP_TITLE", "My FastAPI App")  # Default title
    
    # Return the app info as JSON
    return AppInfo(app_version=app_version, app_title=app_title)
    
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from prometheus_client import Counter
from fastapi import FastAPI
import os
from prometheus_client import generate_latest

app = FastAPI()

request_counter = Counter('request_count', 'Total number of requests')

@app.get("/get_info")
async def get_info():
    request_counter.inc()
    app_version = os.getenv("APP_VERSION", "1.0")
    app_title = os.getenv("APP_TITLE", "My FastAPI App")
    return {"app_version": app_version, "app_title": app_title}

@app.get("/metrics")
async def metrics():
    return generate_latest(request_counter)

