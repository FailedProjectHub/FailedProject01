from django.shortcuts import render


def indexpage(request):
    return render(request, 'index.html')
