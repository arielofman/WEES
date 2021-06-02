from django.shortcuts import render

def error404(request, exception): 
	return render(request, 'commons/error404.html', status=404) 