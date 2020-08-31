
from django.conf.urls import url
from django.urls import  path
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.websocket import consumers


websocket_urlPattern = [
	path("ws/messages/", consumers.ChatConsumer, name='web-chat'),

]

# application = [websocket_urlPattern]
application = ProtocolTypeRouter({ 
	# Websocket chat handler
	'websocket': 
		# AllowedHostsOriginValidator(
			AuthMiddlewareStack(
				URLRouter( websocket_urlPattern )
			),
		# ),
})

 