
from django.http import HttpResponse
from django.shortcuts import redirect



def unauthanticated_user(view_fn):
    def wrapper_fn(request, *args, **kwargs):
           if request.user.is_authenticated:
             return redirect('home')
           else:
               return view_fn(request,*args, **kwargs)
    return wrapper_fn

# this function restrict user from all functionalities


def authorized_user(allowed_roles=[]):
    def decorator(view_fn):
        def wrapper_fn(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_fn(request,*args, **kwargs)
            else:
                return HttpResponse("you are not allowed to view this page")
        return wrapper_fn
    return decorator




def admin_only(view_fn):
    
        def wrapper_fn(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == 'customer':
                return redirect('user')
            
            if group == 'admin':
                return view_fn (request,*args, **kwargs)
                
        return wrapper_fn
    