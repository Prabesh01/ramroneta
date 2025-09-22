from django.shortcuts import render
from .models import Candidate, Case, Kartut, Party,  Representative
from django.db.models import Count

def home(request):
    return render(request, 'home.html')

def hor_home(request, year):
    return render(request, 'hor_home.html', {'year': year})

def hor_constituencies(request, year):
    return render(request, 'hor_constituencies.html', {'year': year})

def hor_fptp_candidate_detail(request, year, constituency, candidate_id):
    pass

def hor_parties(request, year):
    parties = Party.objects.filter(
        representative__year=year, # representative__proportional=True
    ).annotate(
        rep_count=Count('representative')
    ).distinct().order_by('-rep_count', 'name')

    return render(request, 'party_list.html', {'year': year, 'parties': parties})

def hor_pr_candidate_detail(request, year, party, candidate_id):
    pass