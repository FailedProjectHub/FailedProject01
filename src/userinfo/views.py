from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.


class register(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return HttpResponse("please first logout")
        else:
            return super(register, self).dispatch(request, *args, **kwargs)
