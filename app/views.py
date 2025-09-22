from django.shortcuts import render
from .models import Candidate, Case, Kartut, Party,  Representative
from django.db.models import Count
from collections import defaultdict

def home(request):
    return render(request, 'home.html')

def hor_home(request, year):
    return render(request, 'hor_home.html', {'year': year})

def hor_constituencies(request, year):
    return render(request, 'hor_constituencies.html', {'year': year})

def hor_fptp_candidate_detail(request, year, constituency, candidate_id):
    fptp_candidates = Representative.objects.filter(year=year, hor_constituency=constituency, proportional=False)

    try:
        target = Representative.objects.select_related(
            'candidate', 'party'
        ).get(
            candidate__id=candidate_id,
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
        target = cases = kartuts = case_counts = total_cases = other_cases_count = None

    return render(request, 'candidate.html', {'year': year, 'constituency': constituency, 'candidates': fptp_candidates, 'target': target, 'cases': cases, 'kartuts': kartuts, 'case_counts': case_counts, 'total_cases': total_cases, 'other_cases_count': other_cases_count})

def hor_parties(request, year):
    parties = Party.objects.filter(
        representative__year=year, # representative__proportional=True
    ).annotate(
        rep_count=Count('representative')
    ).distinct().order_by('-rep_count', 'name')

    return render(request, 'party_list.html', {'year': year, 'parties': parties})

def hor_pr_candidate_detail(request, year, party, candidate_id):
    pass