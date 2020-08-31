from django.shortcuts import render
from django.http import HttpResponse




def home(request):
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