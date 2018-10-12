import vk
import requests
from google_images_download import google_images_download
import json
import os

def longpolling():
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

		print(response)

		if response['updates']:
			for action in response['updates']:
				print(action)
				if len(action) <= 4 or action[6].get('from_admin'):
					continue
				api.messages.send(user_id=action[3], message=action[5], v=api_version)
				arguments = {"keywords":action[5],"limit":1,"print_urls":True}
				urls = google_images_download.googleimagesdownload().download(arguments)
				print(action)
				print(urls)



if __name__ == '__main__':
	session = vk.Session(access_token=os.environ['SECRET_KEY'])
	api = vk.API(session)
	api_version = 5.85

	longpolling()
