from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.type in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.type == "ADMIN":
			return view_func(request, *args, **kwargs)
		else:
			# return HttpResponse('You are not authorized to view this page')
			return render(request, '403.html')

	return wrapper_function

def supervisor_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.type == "SUPERVISOR":
			return view_func(request, *args, **kwargs)
		else:
			# return HttpResponse('You are not authorized to view this page')
			return render(request, '403.html')

	return wrapper_function

def sales_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.type == "SALES":
			return view_func(request, *args, **kwargs)
		else:
			# return HttpResponse('You are not authorized to view this page')
			return render(request, '403.html')

	return wrapper_function