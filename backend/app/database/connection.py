import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

ORDS_BASE_URL = os.getenv("ORDS_BASE_URL", "https://oracleapex.com/ords/biocompost").rstrip("/")

def fetch_ords(endpoint: str, method: str = "GET", data: dict = None):
    clean_endpoint = endpoint.strip("/")
    url = f"{ORDS_BASE_URL}/{clean_endpoint}/"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, verify=False, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, verify=False, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, verify=False, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, verify=False, timeout=30)
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as exc:
        raise Exception(f"HTTP {response.status_code} desde ORDS ({url}): {response.text}")
    except Exception as exc:
        raise Exception(f"Error al conectar con ORDS ({url}): {str(exc)}")