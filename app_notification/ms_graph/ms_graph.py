import webbrowser
from datetime import datetime
import json
import os
import msal

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'


# def generate_access_token(app_id, tenant_id, client_credential):
#     # Define the authority URL with the tenant ID
#     authority = f"https://login.microsoftonline.com/{tenant_id}"
#     # Save Session Token as a token file
#     access_token_cache = msal.SerializableTokenCache()
#
#     # Read the token file if it exists
#     if os.path.exists('ms_graph_api_token.json'):
#         with open("ms_graph_api_token.json", "r") as token_file:
#             access_token_cache.deserialize(token_file.read())
#
#         token_detail = json.load(open('ms_graph_api_token.json'))
#         if 'AccessToken' in token_detail:
#             token_detail_key = list(token_detail['AccessToken'].keys())[0]
#             token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
#             if datetime.now() > token_expiration:
#                 os.remove('ms_graph_api_token.json')
#                 access_token_cache = msal.SerializableTokenCache()
#
#     # Assign the SerializableTokenCache object to the client instance
#     client = msal.ConfidentialClientApplication(
#         client_id=app_id,
#         token_cache=access_token_cache,
#         authority=authority,
#         client_credential=client_credential,
#     )
#
#     accounts = client.get_accounts()
#     # The /.default scope is used for client credentials flow
#     scopes = ["https://graph.microsoft.com/.default"]
#
#     if accounts:
#         # Load the session
#         token_response = client.acquire_token_silent(scopes=scopes, account=accounts[0])
#     else:
#         # Get the token with client credentials
#         token_response = client.acquire_token_for_client(scopes=scopes)
#     # Save the token cache to the file
#     with open('ms_graph_api_token.json', 'w') as token_file:
#         token_file.write(access_token_cache.serialize())
#
#     return token_response
def generate_access_token(app_id, client_secret, tenant_id):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    
    app = msal.ConfidentialClientApplication(
        client_id=app_id,
        client_credential=client_secret,
        authority=authority
    )

    scopes = ["https://graph.microsoft.com/.default"]
    token_response = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in token_response:
        return token_response
    else:
        raise Exception(f"Could not obtain access token: {token_response}")
    

def generate_public_access_token(app_id, scopes):
    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # # read the token file
    # if os.path.exists('ms_graph_api_token.json'):
    #     access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
    #     token_detail = json.load(open('ms_graph_api_token.json',))
    #     token_detail_key = list(token_detail['AccessToken'].keys())[0]
    #     token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
    #     if datetime.now() > token_expiration:
    #         os.remove('ms_graph_api_token.json')
    #         access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authetnicate your accoutn as usual
        flow = client.initiate_device_flow(scopes=scopes)
        print('user_code: ' + flow['user_code'])
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response
