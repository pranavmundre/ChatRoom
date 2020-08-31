import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async

# from chat.models import Thread, ChatMessage


User = get_user_model()


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

import json

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self ):
		# print("Websocket: connected",text_data )
		await self.accept()
		await self.send(json.dumps({
					"type": "websocket.accept"
				}))
		


	async def receive(self, text_data ):
		message_data = {}
		text_data = json.loads(text_data)
		# print("ok", text_data['message'])

		try:
			if "create_user_chat" == text_data.get('action', "") :
				self.group_name = text_data['group_name']

				await self.channel_layer.group_add(
		           self.group_name,
		           self.channel_name
		       )
				action = "new_user_added"
			else:
				action = "message"

		except Exception as e:
			# raise e
			pass
		message_data['username'] = text_data.get("username", "Anonymous")
		message_data['group_name'] =self.group_name
		message_data['message'] = text_data.get("message", "Anonymous")

		await self.channel_layer.group_send(
			self.group_name,
			{
				'type': 'send_msg',
				'group_name' : self.group_name, 
				'message' : message_data, 
				'action' : action, 
			}
		)
		print("Websocket: ",text_data )
		

	async def disconnect(self, close_code):
		# print("Websocket: disconnected",)
		# await self.disconnect()
		pass


	async def send_msg(self, event):
		try:
			# print("event: ", event)
			message = event['message']

			await self.send(text_data=json.dumps({
					'message_data': message, 
					'action': event['action'], 
				}))
		except Exception as e:
			raise e
			# print("Error: ", e)
		pass

	async def create_room(self, event):
		pass