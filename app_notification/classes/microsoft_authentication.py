import msal
from django.conf import settings


class MSAuthentication:
	def __init__(self):
		self.app_id = settings.MS_APP_ID
		self.client_secret = settings.CLIENT_SECRET
		self.tenant_id = settings.MS_TENANT_ID
		self.endpoint = settings.GRAPH_API_ENDPOINT
	
	def _generate_access_token(self):
		authority = f"https://login.microsoftonline.com/{self.tenant_id}"
		
		app = msal.ConfidentialClientApplication(
			client_id=self.app_id,
			client_credential=self.client_secret,
			authority=authority
		)
		
		scopes = ["https://graph.microsoft.com/.default"]
		token_response = app.acquire_token_for_client(scopes=scopes)
		
		if "access_token" in token_response:
			return token_response
		else:
			raise Exception(f"Could not obtain access token: {token_response}")
	
	def get_authorization_header(self):
		token_response = self._generate_access_token()
		token = token_response['access_token']
		return {
			"Authorization": f"Bearer {token}",
			"Content-Type": "application/json"
		}
