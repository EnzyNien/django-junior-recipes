from functools import wraps

def add_userdata_to_context(func):
	@wraps(func)
	def wrap(request, *args,**kwargs):
		print(f'request = {request}')
		print(f'request.user = {request.user}')
		print(f'args = {args}')
		print(f'kwargs = {kwargs}')
		user = request.user
		add_userdata_to_context_dict = {
			'user':user,
			'is_authenticated':user.is_authenticated
		}
		setattr(wrap,'context',add_userdata_to_context_dict)
		return func(request, *args,**kwargs)
	return wrap
