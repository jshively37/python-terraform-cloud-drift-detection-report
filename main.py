import os
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
except ImportError:
    print("python-dotenv not found")

TFCB_SLUGS = {
    "list_orgs": "/api/v2/organizations",
    "list_workspaces": f"/api/v2/organizations/{TFCB_ORG}/workspaces"
}

TFCB_HEADERS = {
    "Authorization": f"Bearer {TFCB_API_KEY}"
}


def make_request(slug, headers=TFCB_HEADERS, method="GET"):
    url = TFCB_PATH + slug
    response = requests.request(method, url, headers=headers)
    try:
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        print(e)


def retrieve_workspaces():
    """_summary_
    """
    # Create the URL
    slug = TFCB_SLUGS['list_workspaces']
    response = make_request(slug)
    for workspace in response['data']:
        drift_status_url = ""
        drift_status = ""
        drift_ran_date = ""
        workspace_name = workspace['attributes']['name']
        if drift_configured := workspace['attributes']['drift-detection']:
            drift_status_url = workspace['relationships']['current-assessment-result']['links']['related']
            drift_response = make_request(drift_status_url)
            drift_status = drift_detected(drift_response)
            drift_ran_date = drift_last_ran(drift_response)
        print(workspace_name, drift_status, drift_ran_date)


def drift_detected(drift_response):
    """_summary_
    """
    return drift_response['data']['attributes']['drifted']


def drift_last_ran(drift_response):
    """_summary_

    Args:
        drift_response (_type_): _description_

    Returns:
        _type_: _description_
    """
    return drift_response['data']['attributes']['created-at']


if __name__ == "__main__":
    retrieve_workspaces()
