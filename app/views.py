from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def hor_home(request, year):
    return render(request, 'hor_home.html', {'year': year})

def hor_parties(request, year):
    pass

def hor_constituencies(request, year):
    return render(request, 'hor_constituencies.html', {'year': year})