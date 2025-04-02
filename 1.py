from dotenv import load_dotenv
import os

load_dotenv("./.env") 
api_key = os.getenv("Google_Api_key")

if api_key:
    print("API_KEY loaded:", api_key)
else:
    print("API_KEY not found in .env file")
