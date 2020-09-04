from django.urls import path, include
from . import views




urlpatterns = [
	
	# path('test/', views.test ),
	path('live-web/', views.live_web_msg, name="live_web_msg" ),

]


