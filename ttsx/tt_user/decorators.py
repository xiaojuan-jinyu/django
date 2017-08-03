from django.shortcuts import redirect

def decorators(func1):
    def func(request,*args,**kwargs):
        uname = request.session.get('uname',1)
        if uname == 1:
            return redirect('/user/login/')
        else:
            return func1(request,*args,**kwargs)
    return func


