#!/usr/bin/env python3

import requests as r
import json
import logging as l
import settings as s
payload = ''

def buildHeader():
	return{
		'Accept': "application/json",
    	'Content-Type': "application/json",
    	'Authorization': 'SSWS ' + s.APITOKEN,
    	'Host': s.HOST
		}

def send_activation(userId):
	url = f"https://${s.HOST}/api/v1/users/{userId}/lifecycle/reactivate?sendEmail=True"
	l.debug(url)
	headers = buildHeader()
	result = r.request("POST", url, data=payload, headers=headers)
	if result.status_code == 200:
		l.info(f"Activation email sent to user ID: {userId}")
		return True
	else:
		l.info(f"Unable resend activation for user with ID: {userId}")
		return False
	response = json.loads(result.text)
	l.debug(f"Activation sent: {userId} - Status: {response['status']}")
	return True

def get_pending_users():
	url = f'https://{s.HOST}/api/v1/users?filter=status eq "PROVISIONED"'
	l.debug(url)
	headers = buildHeader()
	result = r.request("GET", url, headers=headers)
	if result.status_code != 200:
		l.error(f"Unable to retrieve users")
		return False
	response = json.loads(result.text)
	for user in response:
		if user['lastLogin'] == None:
			send_activation(user['id'])

def main():
	l.info('-- Start')
	get_pending_users()

if __name__ == '__main__':
	main()