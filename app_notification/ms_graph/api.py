import asyncio

import requests
from msgraph.generated.models.calendar import Calendar
from msgraph.generated.models.event import Event
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.location import Location
from msgraph.generated.models.attendee import Attendee
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.attendee_type import AttendeeType
from rich import console
from ms_graph import generate_access_token, GRAPH_API_ENDPOINT, generate_public_access_token
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

credentials = ClientSecretCredential(
	'd11d44f9-972d-4ae1-9c77-092a048d2a2e',
	'2571aefd-8841-4932-b741-99b6bb14a428',
	'38B8Q~TfTNxz0aCNKimzwsVdrLxBNsEne2r4YaP5',
)
# scopes = ['https://graph.microsoft.com/.default']
scopes = [
	'https://graph.microsoft.com/Calendars.ReadWrite',
	'https://graph.microsoft.com/User.ReadWrite.All',
]

client = GraphServiceClient(credentials=credentials, scopes=scopes)

console = console.Console()
APP_ID = '2571aefd-8841-4932-b741-99b6bb14a428'
TENANT_ID = 'd11d44f9-972d-4ae1-9c77-092a048d2a2e'
CLIENT_SECRET = '38B8Q~TfTNxz0aCNKimzwsVdrLxBNsEne2r4YaP5'

# graph_client = GraphServiceClient(credentials, scopes)
# Step 1: Generate access token
access_token = generate_access_token(APP_ID, CLIENT_SECRET, TENANT_ID)


# console.print(access_token)
# access_token = generate_public_access_token(APP_ID, scopes)


# Step 2: Get create an event
def create_ms_event(event_title, **event_details):
	request_body = {
		'subject': event_title
	}
	for key, val in event_details.items():
		request_body[key] = val
	return request_body


def create_event_for_user(token_response, user_id, event_title, event_details):
	endpoint = f"{GRAPH_API_ENDPOINT}/users/{user_id}/events"
	token = token_response['access_token']
	headers = {
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json"
	}
	event_body = create_ms_event(event_title, **event_details)
	response = requests.post(endpoint, headers=headers, json=event_body)
	if response.status_code == 201:
		print("Event created successfully")
	else:
		print(f"Failed to create event: {response.status_code}, {response.json()}")
	return response.json()


def get_calendar_events(token_response, user_id):
	endpoint = f"{GRAPH_API_ENDPOINT}/users/{user_id}/calendar/events"
	token = token_response['access_token']
	headers = {"Authorization": f"Bearer {token}"}
	response = requests.get(endpoint, headers=headers)
	if response.status_code == 200:
		return response.json()
	else:
		print(f"Failed to fetch calendar events: {response.status_code}, {response.json()}")
		return None


def calendar_events(token_response, user_id):
	# Construct the endpoint URL
	endpoint = f"{GRAPH_API_ENDPOINT}/users/{user_id}/events"
	
	# Extract the access token from the token response
	token = token_response.get('access_token')
	
	# Verify the token is not None
	if not token:
		print("Error: Access token is missing or invalid.")
		return None
	
	# Set up the request headers with the authorization token
	headers = {"Authorization": f"Bearer {token}"}
	
	try:
		# Make the GET request to fetch calendar events
		response = requests.get(endpoint, headers=headers)
		
		# Check if the response is successful
		if response.status_code == 200:
			return response.json()
		else:
			# Handle different error statuses with more specific messages
			error_info = response.json()
			if response.status_code == 401:
				print(f"Unauthorized access: {error_info}")
			elif response.status_code == 404:
				print(f"Resource not found: {error_info}")
			else:
				print(f"Failed to fetch calendar events: {response.status_code}, {error_info}")
			return None
	except requests.RequestException as e:
		print(f"An error occurred: {e}")
		return None


event_title = "Test Event"
event_details = {
	'start': {'dateTime': '2024-05-29T12:00:00', 'timeZone': 'UTC'},
	'end': {'dateTime': '2024-05-29T13:00:00', 'timeZone': 'UTC'}
}


def fetch_user_id(email, token_response):
	endpoint = f"{GRAPH_API_ENDPOINT}/users?$filter=mail eq '{email}'"
	token = token_response['access_token']
	headers = {
		"Authorization": f"Bearer {token}"
	}
	response = requests.get(endpoint, headers=headers)
	if response.status_code == 200:
		return response.json()
	else:
		print(f"Failed to fetch user ID for {email}: {response.status_code}, {response.json()}")
		return None


user = fetch_user_id('motlhankamoffat@gmail.com', access_token)
user_id = user['value'][0]['id']

console.print(user_id)


# if user_id:
# 	console.print(calendar_events(access_token, user_id))
# create_event_for_user(access_token, user_id, event_title, event_details)
# async def get_user():
# 	user = await client.users.by_user_id(user_id).get()
# 	if user:
# 		print(user.display_name)
#

# asyncio.run(get_user())


# async def create_event():
# 	graph_client = GraphServiceClient(credentials, scopes)
# 	# request_body = Event(
# 	# 	subject="Let's go for lunch",
# 	# 	body=ItemBody(
# 	# 		content_type=BodyType.Html,
# 	# 		content="Does mid month work for you?",
# 	# 	),
# 	# 	start=DateTimeTimeZone(
# 	# 		date_time="2019-03-15T12:00:00",
# 	# 		time_zone="Pacific Standard Time",
# 	# 	),
# 	# 	end=DateTimeTimeZone(
# 	# 		date_time="2019-03-15T14:00:00",
# 	# 		time_zone="Pacific Standard Time",
# 	# 	),
# 	# 	location=Location(
# 	# 		display_name="Harry's Bar",
# 	# 	),
# 	# 	attendees=[
# 	# 		Attendee(
# 	# 			email_address=EmailAddress(
# 	# 				address="adelev@contoso.com",
# 	# 				name="Adele Vance",
# 	# 			),
# 	# 			type=AttendeeType.Required,
# 	# 		),
# 	# 	],
# 	# 	transaction_id="7E163156-7762-4BEB-A1C6-729EA81755A7",
# 	# )
# 	request_body = Calendar(
# 		name="Volunteer",
# 	)
#
# 	result = await graph_client.users.by_user_id(user_id).calendars.post(request_body)
# 	console.print(result)
# 	return result
#
#
# asyncio.run(create_event())

console.print(calendar_events(access_token, user_id))
