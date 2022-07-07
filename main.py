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
    return api_request(slug)

def parse_workspace_response(response):
    drift_payload = []
    for workspace in response['data']:
        drift_status_url = ""
        drift_detected = ""
        drift_ran_date = ""
        workspace_name = workspace['attributes']['name']
        if drift_configured := workspace['attributes']['drift-detection']:
            # If drift was corrected recently but a new drift assesment has not occured the links key
            # is not available in the payload. This section handles those cases and sets drift_detected
            # to pending run. It might take 24 hours for TFCB to perform a new drift run.
            try:
                drift_status_url = workspace['relationships']['current-assessment-result']['links']['related']
                drift_response = api_request(drift_status_url)
                drift_detected = drift_response['data']['attributes']['drifted']
                drift_ran_date = drift_response['data']['attributes']['created-at'].split(".")[0]
            except KeyError:
                drift_detected = "pending_new_drift_run"
                print(f"Workspace: {workspace_name} has drift enabled but pending drift run")
        drift_payload.append({
            "workspace_name": workspace_name,
            "drift_configured": drift_configured,
            "drift_detected": drift_detected,
            "drift_last_checked": drift_ran_date
        })
    return drift_payload


def create_csv(drift_payload):
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    keys = drift_payload[0].keys()
    filename = f"{OUTPUT_DIR}/drift_{date}.csv"
    with open(filename, "w") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(drift_payload)
    print(f"Wrote output file: {filename}")


if __name__ == "__main__":
    # Check if output directory exists and if not create it
    if not os.path.isdir(OUTPUT_DIR):
        print("Output directory does not exist. Creating output directory")
        os.makedirs(OUTPUT_DIR)
    workspace_reponse = retrieve_workspaces()
    drift_payload = parse_workspace_response(workspace_reponse)
    create_csv(drift_payload)
