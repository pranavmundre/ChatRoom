from django.shortcuts import render
from django.http import HttpResponse
from chat.websocket.consumers import SocketIO
from chat.websocket.consumers import sio
import asyncio
import time

from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync


def home(request):
	# sio.emit("notfiy", "ok")
	return render( request, "index.html" )

def live_web_msg(request):
	username = request.GET.get("username", "Anonymous")
	group_name = request.GET.get("group_name", "Anonymous")

	# print("Ok: ", group_name)
	context = {
		"username": username,
		"group_name": group_name,
	}

	return render( request, "live-chat.html", context )
