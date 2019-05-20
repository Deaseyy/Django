from functools import wraps

from django.http import HttpResponseRedirect


def islogin(func):
    @wraps(func)
    def check(request):
        if not request.session.get('username'):
            return HttpResponseRedirect('/user/login/')
        return func(request)
    return check