from django.shortcuts import render


def register(request):
    return render(request,"index.html")

def signin(request):
    return render(request,"signin.html")
# Create your views here.
