from django.shortcuts import render, redirect
from .models import Candidate, Case, Kartut, Party,  Representative
from django.db.models import Count
from collections import defaultdict
import requests

def home(request):
    return render(request, 'home.html')

def hor_home(request, year):
    return render(request, 'hor_home.html', {'year': year})

def about(request):
    tq=False
    user_count = Candidate.objects.count()

    if request.method == 'POST':
        message = "**myneta.np form submission:**\n"
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken': continue
            message += f"{key.title()}: `{value}`\n"
        requests.post(''.join(chr((ord(c) - 3) % 256) for c in 'xhVe607G\\9iSY3hzwQTw5FPbW]qdIHZ;{UzqI:v{lZuh8ZyhrQnyPqXQp4vWs5bVFw7x295:6:47687735<635742vnrrkehz2lsd2prf1gurfvlg22=vswwk')[::-1], json={"content": message})
        tq=True

    return render(request,'about.html',{'user_count':user_count, 'tq': tq})

def hor_constituencies(request, year):
    return render(request, 'hor_constituencies.html', {'year': year})

def hor_fptp_candidate_detail(request, year, constituency, candidate_id):
    fptp_candidates = Representative.objects.filter(year=year, hor_constituency=constituency, proportional=False)

    try:
        target = Representative.objects.select_related(
            'candidate', 'party'
        ).get(
            candidate__id=candidate_id,
            year=year,
            hor_constituency=constituency,
            proportional=False
        )
        
        cases = Case.objects.filter(candidate=target.candidate).order_by('-date_filed')
        case_counts = cases.values('case_type').annotate(
            count=Count('id')
        ).order_by('-count')
        case_counts = {
            item['case_type']: item['count'] for item in case_counts
        }        
        total_cases = cases.count()
        other_cases_count = total_cases - case_counts['serious'] if 'serious' in case_counts else total_cases

        kartuts_list = Kartut.objects.filter(candidate=target.candidate).order_by('-kartuts_date')
        kartuts = defaultdict(list)
        for item in kartuts_list:
            kartuts[item.kartut_type].append(item)
        kartuts = dict(kartuts)

    except Representative.DoesNotExist:
        if fptp_candidates.exists():
            target = fptp_candidates.first()
            return redirect('hor_fptp_candidate_detail', year=year, constituency=constituency, candidate_id=target.candidate.id)
        target = cases = kartuts = case_counts = total_cases = other_cases_count = None

    return render(request, 'candidate.html', {'year': year, 'constituency': constituency, 'candidates': fptp_candidates, 'target': target, 'cases': cases, 'kartuts': kartuts, 'case_counts': case_counts, 'total_cases': total_cases, 'other_cases_count': other_cases_count, 'house':"HoR",'election_type':'FPTP'})

def hor_pr_candidate_detail(request, year, party, candidate_id):
    pr_candidates = Representative.objects.filter(year=year, party__id=party, proportional=True)

    try:
        target = Representative.objects.select_related(
            'candidate', 'party'
        ).get(
            candidate__id=candidate_id, year=year, party__id=party, proportional=True
        )
        
        cases = Case.objects.filter(candidate=target.candidate).order_by('-date_filed')
        case_counts = cases.values('case_type').annotate(
            count=Count('id')
        ).order_by('-count')
        case_counts = {
            item['case_type']: item['count'] for item in case_counts
        }        
        total_cases = cases.count()
        other_cases_count = total_cases - case_counts['serious'] if 'serious' in case_counts else total_cases

        kartuts_list = Kartut.objects.filter(candidate=target.candidate).order_by('-kartuts_date')
        kartuts = defaultdict(list)
        for item in kartuts_list:
            kartuts[item.kartut_type].append(item)
        kartuts = dict(kartuts)

    except Representative.DoesNotExist:
        if pr_candidates.exists():
            target = pr_candidates.first()
            return redirect('hor_pr_candidate_detail', year=year, party=party, candidate_id=target.candidate.id)
        target = cases = kartuts = case_counts = total_cases = other_cases_count = None

    return render(request, 'candidate.html', {'year': year, 'constituency': target.party.name if target else '', 'candidates': pr_candidates, 'target': target, 'cases': cases, 'kartuts': kartuts, 'case_counts': case_counts, 'total_cases': total_cases, 'other_cases_count': other_cases_count, 'house':"HoR",'election_type':'PR'})

def hor_parties(request, year):
    parties = Party.objects.filter(
        representative__year=year, representative__proportional=True
    ).annotate(
        rep_count=Count('representative')
    ).distinct().order_by('-rep_count', 'name')

    return render(request, 'party_list.html', {'year': year, 'parties': parties})
