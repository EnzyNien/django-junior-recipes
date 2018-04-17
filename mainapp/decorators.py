from functools import wraps

def user_login(func):
	@wraps(func)
	def wrap(request, *args,**kwargs):
		print(f'request = {request}')
		print(f'request.user = {request.user}')
		print(f'args = {args}')
		print(f'kwargs = {kwargs}')
		user = request.user
		user_login_dict = {
			'user':user,
			'is_authenticated':user.is_authenticated
		}
		setattr(wrap,'context',user_login_dict)
		return func(request, *args,**kwargs)
	return wrap
