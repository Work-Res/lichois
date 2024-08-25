import requests


def get_oauth2_token(client_id, client_secret, tenant_id):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "client_id": client_id,
        "scope": "https://outlook.office365.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()

    return response.json()["access_token"]
