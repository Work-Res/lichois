import requests

from .microsoft_authentication import MSAuthentication


class MicrosoftEvent:
	
	def __init__(self,  event):
		self.auth = MSAuthentication()
		self.event = event
		
	def create_event(self):
		endpoint = f"{self.auth.endpoint}/me/calendar/events"
		headers = self.auth.get_authorization_header()
		event_body = self.event
		response = requests.post(endpoint, headers=headers, json=event_body)
		if response.status_code == 201:
			print("Event created successfully")
		else:
			print(f"Failed to create event: {response.status_code}, {response.json()}")
		return response.json()
	
	def fetch_user_id(self, email):
		endpoint = f"{self.auth.endpoint}/users?$filter=mail eq '{email}'"
		response = requests.get(endpoint, headers=self.auth.get_authorization_header())
		if response.status_code == 200:
			print(response.json())
			return response.json()
		else:
			print(f"Failed to fetch user ID for {email}: {response.status_code}, {response.json()}")
			return None
	




