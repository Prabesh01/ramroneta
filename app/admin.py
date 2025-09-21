from django.contrib import admin
from .models import Candidate, Case, Kartut, Representative, Party
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import Q

def mod_perm_check(request,obj):
    reps = Representative.objects.filter(candidate=obj.candidate)
    if not reps.exists(): 
        return False
    
    valid_username = False
    for rep in reps:
        if rep.hor_constituency.startswith(request.user.username) or rep.province_constituency.startswith(request.user.username):
            valid_username = True
            break

    if not valid_username:
        return False

    return True

class CandidateAdmin(admin.ModelAdmin):
    # display these columns
    list_display = ('name',)
    # searchable in admin panel and enable dropdown search for other tables
    search_fields = ('name',)
    # sidebar filter
    # list_filter = ('name',)

    # non super user cannot view or alter unauthorized Candidates.
    # but on other tables, even if they can only view their own candidates in dropdown, 
    # they can still set unauthorized candidates by editing network requests.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        return qs.filter(
            Q(added_by=request.user) |
            Q(representative__hor_constituency__startswith=request.user.username) |
            Q(representative__province_constituency__startswith=request.user.username)
        ).distinct()

    # since added_by is non-editable field, it shall be set here.
    def save_model(self, request, obj, form, change):
        if not obj.pk: obj.added_by = request.user
        super().save_model(request, obj, form, change)

class CaseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['candidate']

    list_display = ('candidate', 'case_number')
    search_fields = ('case_number', 'candidate__name')
    list_filter = ('case_type','court',)

    # get_queryset: self constituency only.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        return qs.filter(
            Q(candidate__representative__hor_constituency__startswith=request.user.username) |
            Q(candidate__representative__province_constituency__startswith=request.user.username)
        ).distinct()

    # even if unauthorised candidates arent displayed in dropdown,
    # mods might change candidate id in network request to set case for unauthorized candidates
    # this code avoids that scenario.
    def save_model(self, request, obj, form, change):
        if not mod_perm_check(request,obj):
            raise ValidationError('You are not allowed to set case for that candidate')
        super().save_model(request, obj, form, change)


class KartutAdmin(admin.ModelAdmin):
    autocomplete_fields = ['candidate', 'party']

    list_display = ('candidate__name', 'party__name', 'kartut_type', 'kartuts_date')
    search_fields = ('candidate__name', 'party__name',)
    list_filter = ('kartut_type',)

    # get_queryset: self constituency only.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        return qs.filter(
            Q(candidate__representative__hor_constituency__startswith=request.user.username) |
            Q(candidate__representative__province_constituency__startswith=request.user.username)
        ).distinct()

    # hide party field.
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            for field_name, field in form.base_fields.items():
                if field_name in ['party']:
                    field.widget = forms.HiddenInput()
        return form
    
    def save_model(self, request, obj, form, change):
        if not mod_perm_check(request,obj):
            raise ValidationError('You are not allowed to set Kartut for that candidate')

        if not request.user.is_superuser:
            for field in form.changed_data:
                if field in ['party']:
                    raise ValidationError('You are not allowed to change these fields')                 
        return super().save_model(request, obj, form, change)        


class RepresentativeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['candidate', 'party']

    list_display = ('candidate', 'house','hor_constituency','province_constituency')
    search_fields = ('candidate__name',)
    list_filter = ('house',)

    # get_queryset: self constituency only.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        return qs.filter(
            Q(candidate__representative__hor_constituency__startswith=request.user.username) |
            Q(candidate__representative__province_constituency__startswith=request.user.username)
        ).distinct()

    def save_model(self, request, obj, form, change):
        if not obj.candidate.added_by != request.user: 
            raise ValidationError('You are not allowed to set Representative for that candidate')
        if obj.hor_constituency.startswith(request.user.username) or obj.province_constituency.startswith(request.user.username):
            super().save_model(request, obj, form, change)
        else: raise ValidationError('You are not allowed to set Representative of that constituency')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Kartut, KartutAdmin)
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Party, PartyAdmin)