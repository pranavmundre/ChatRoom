import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync


User = get_user_model()

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
		

	async def disconnect(self, close_code):
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

	
class SocketIO( AsyncWebsocketConsumer ):
	async def connect(self ):
		self.group_name = "all"
		await self.channel_layer.group_add(
		   self.group_name,
		   self.channel_name
	   	)
		await self.accept()
		await self.send(json.dumps({
					"type": "websocket.accept",
				}))

	async def receive(self, text_data ):
		# await self.emit('notify',{'k':'asdf'})
		pass

	async def disconnect(self, close_code):
		print("Websocket: disconnected",)
		print("close_code: ", close_code )
		pass

	async def emit(self, *arg , **kwarg):
		await self.channel_layer.group_send(
			"all", 
			{
				'type': 'send_to_all',
				'data':arg, 
			}
		)
	
	async def send_to_all(self, event):
		await self.send(json.dumps(event['data']))

class sio:
	def __init__(self, arg):
		self.group_name = "all"

	@async_to_sync
	async def emit( self, *arg ):
		from channels.layers import get_channel_layer
		channel_layer = get_channel_layer()
		await channel_layer.group_send(
			"all",
			{
				'type': 'send_to_all',
				'data': arg 
			}
		)
		return True
