from django.http import HttpResponse, JsonResponse

def allowed_users(allowed_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args , **kwargs):
      user_role = request.user.profile.role
      if user_role in allowed_roles:  
        return view_func(request, *args , **kwargs)
      else:
        return JsonResponse({'error': 'You do not have permission to access this page'} , status=403)
    return wrapper_func
  return decorator