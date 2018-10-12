import vk
import requests
from google_images_download import google_images_download
import json

with open('config.json', 'r') as f:
	config = json.load(f)

session = vk.Session(access_token=config['SECRET_KEY'])
api = vk.API(session)
api_version = 5.85
long_poll_info = api.messages.getLongPollServer(v=api_version)

while True:

	long_poll_info = api.messages.getLongPollServer(v=api_version)
	response = requests.post(
		"https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode={mode}&version=2".format(
			server=long_poll_info['server'], 
			key=long_poll_info['key'], 
			ts=long_poll_info['ts'], 
			mode=2
			),
		timeout=30
		).json()

	if response['updates']:
		for action in response['updates']:
			print(action)
			if len(action) <= 4 or action[6].get('from_admin'):
				continue
			api.messages.send(user_id=action[3], message=action[5], v=api_version)
			arguments = {"keywords":action[5],"limit":1,"print_urls":True}
			google_images_download.googleimagesdownload().download(arguments)
			print(action)
