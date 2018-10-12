import vk
import requests
from google_images_download import google_images_download
import json
import os

def longpolling(upload_tool):
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
				arguments = {"keywords":action[5],"limit":1,"print_urls":True}
				urls = google_images_download.googleimagesdownload().download(arguments)
				print(action)
				print(urls)
				pic_path = urls[action[5]][0]
				vk_pic_url = upload_tool.document(pic_path)[0]['url']
				api.messages.send(user_id=action[3], message=vk_pic_url, v=api_version)
				os.remove(pic_path)


if __name__ == '__main__':
	session = vk.Session(access_token=os.environ['SECRET_KEY'])
	api = vk.API(session)
	api_version = 5.85

	vk_session = vk_api.VkApi(os.environ['LOGIN'], os.environ['PASS'])
    vk = vk_session.get_api()
    upload_tool = vk_api.VkUpload(vk_session)

	longpolling(upload_tool)
