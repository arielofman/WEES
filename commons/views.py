from django.shortcuts import render

def error404(request): 
	return render(request, 'commons/error404.html', status=404) 