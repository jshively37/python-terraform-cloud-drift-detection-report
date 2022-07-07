import csv
import os
from datetime import datetime
from urllib.error import HTTPError

# Ensure requests is installed
try:
    import requests
except ImportError:
    print("requests not found")

# Ensure dotenv is installed and load variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    TFCB_ORG = os.environ.get("TFCB_ORG")
    TFCB_API_KEY = os.environ.get("TFCB_API_KEY")
    TFCB_PATH = os.environ.get("TFCB_PATH")
    OUTPUT_DIR = os.environ.get("OUTPUT_DIR")
except ImportError:
    print("python-dotenv not found")

# API Endpoints
TFCB_SLUGS = {
    "list_workspaces": f"/api/v2/organizations/{TFCB_ORG}/workspaces"
}

# REST API Header Information
TFCB_HEADERS = {
    "Authorization": f"Bearer {TFCB_API_KEY}"
}


def api_request(slug, headers=TFCB_HEADERS, method="GET"):
    url = TFCB_PATH + slug
    response = requests.request(method, url, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(e)


def retrieve_workspaces():
    slug = TFCB_SLUGS['list_workspaces']
    response = api_request(slug)
    drift_list_dict = []
    for workspace in response['data']:
        drift_status_url = ""
        drift_status = ""
        drift_ran_date = ""
        workspace_name = workspace['attributes']['name']
        if drift_configured := workspace['attributes']['drift-detection']:
            drift_status_url = workspace['relationships']['current-assessment-result']['links']['related']
            drift_response = api_request(drift_status_url)
            drift_status = drift_response['data']['attributes']['drifted']
            drift_ran_date = drift_response['data']['attributes']['created-at'].split(".")[0]
        drift_list_dict.append({
            "workspace_name": workspace_name,
            "drift_configured": drift_configured,
            "drift_status": drift_status,
            "drift_last_checked": drift_ran_date
        })
    return drift_list_dict


def create_csv(drift_list_dict):
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    keys = drift_list_dict[0].keys()
    filename = f"{OUTPUT_DIR}/drift_{date}"
    with open(filename, "w") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(drift_list_dict)


if __name__ == "__main__":
    drift_list_dict = retrieve_workspaces()
    create_csv(drift_list_dict)
