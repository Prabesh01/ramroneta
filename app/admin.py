from django.contrib import admin
from .models import Candidate, Case, Kartut, Representative, Party, HoR_Constituency, Province_Constituency, Municipality, District
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import Value, CharField, Q
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.db.models.functions import Concat

class UserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)

    def has_add_permission(self, request):
        if request.user.is_superuser: return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser: return True
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            for field_name, field in form.base_fields.items():
                if field_name not in ['password']:
                    field.widget = forms.HiddenInput()
                    field.required = False
        return form
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            for field in form.changed_data:
                if field not in ['password']:
                    raise ValidationError('You are not allowed to change these fields')

        return super().save_model(request, obj, form, change)    

    # def has_change_permission(self, request, obj=None):
    #     return True

class GroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser: return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser: return True
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)        

def mod_perm_check(request,obj):
    if request.user.is_superuser: return True

    reps = Representative.objects.filter(candidate=obj.candidate)
    if not reps.exists(): 
        return False

    username = request.user.username
    valid_username = False
    if username.startswith('pr-'):
        party_code = int(username.split('-')[-1])
        for rep in reps:
            if rep.proportional and rep.party.id==party_code:
                valid_username = True
                break
    else:
        user_prefix = username.upper()
        for rep in reps:
            if (
                rep.hor_constituency
                and rep.hor_constituency.startswith(user_prefix)
            ) or (
                rep.province_constituency
                and rep.province_constituency.startswith(user_prefix)
            ) or (
                rep.municipality
                and rep.municipality.district.name.lower().startswith(username.lower())
            ) or (
                rep.municipality
                and rep.municipality.__str__().lower().startswith(username.replace('_',' ').replace('@',', ').lower())
            ):
                valid_username = True
                break

    if not valid_username:
        return False

    return True

def mod_qs(qs,request):
    if request.user.is_superuser: return qs

    username = request.user.username

    if username.startswith('pr-'):
        party_code = int(username.split('-')[-1])
        return qs.filter(
            Q(candidate__representative__party__id=party_code) &
            Q(candidate__representative__proportional=True)
        ).distinct()

    user_prefix = username.upper()
    return qs.annotate(
        full_display=Concat(
        'candidate__representative__municipality__name', 
        Value(', '), 
        'candidate__representative__municipality__district__name',
        output_field=CharField()
    )).filter(
        Q(candidate__representative__hor_constituency__startswith=user_prefix) |
        Q(candidate__representative__province_constituency__startswith=user_prefix) |
        Q(candidate__representative__municipality__district__name__istartswith=username) |
        Q(full_display__istartswith=username.replace('_',' ').replace('@',', '))
    ).distinct()

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

        username = request.user.username

        if username.startswith('pr-'):
            party_code = username.split('-')[-1] # extract party code from username
            # filter the candidates added by user name starting with 'pr-' and ending with '-party_code'
            return qs.filter(added_by__username__endswith='-'+party_code)

        user_prefix = username.upper()
        return qs.annotate(
            full_display=Concat(
                'representative__municipality__name', 
                Value(', '), 
                'representative__municipality__district__name',
                output_field=CharField()
            )
        ).filter(
            Q(added_by=request.user) |
            Q(representative__hor_constituency__startswith=user_prefix) |
            Q(representative__province_constituency__startswith=user_prefix) |
            Q(representative__municipality__district__name__istartswith=username) |
            Q(full_display__istartswith=username.replace('_',' ').replace('@',', '))
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
        return mod_qs(qs, request)

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
        return mod_qs(qs, request)

    # hide party field.
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and not request.user.username.startswith('pr-'):
            for field_name, field in form.base_fields.items():
                if field_name in ['party']:
                    field.widget = forms.HiddenInput()
        return form
    
    def save_model(self, request, obj, form, change):
        if not mod_perm_check(request,obj):
            raise ValidationError('You are not allowed to set Kartut for that candidate')

        if request.user.username.startswith('pr-'):
            party_code = int(request.user.username.split('-')[-1]) # extract party code from username
            if obj.party and obj.party.id != party_code:
                raise ValidationError('You are not allowed to set Kartut for that party')

        elif not request.user.is_superuser:
            for field in form.changed_data:
                if field in ['party']:
                    raise ValidationError('You are not allowed to change these fields')                 
        return super().save_model(request, obj, form, change)        


class RepresentativeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['candidate', 'party']

    list_display = ('candidate', 'house','hor_constituency','province_constituency')
    search_fields = ('candidate__name',)
    list_filter = ('house',)

    class Media:
        js = ('admin/js/representative_admin.js',)

    # get_queryset: self constituency only.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        username = request.user.username

        if username.startswith('pr-'):
            party_code = username.split('-')[-1]
            return qs.filter(
                Q(party__id=party_code) &
                Q(proportional=True)
            )

        user_prefix = username.upper()
        return qs.annotate(
                full_display=Concat(
                'candidate__representative__municipality__name', 
                Value(', '), 
                'candidate__representative__municipality__district__name',
                output_field=CharField()
        )).filter(
            Q(candidate__representative__hor_constituency__startswith=user_prefix) |
            Q(candidate__representative__province_constituency__startswith=user_prefix) |
            Q(candidate__representative__municipality__district__name__istartswith=username) |
            Q(full_display__istartswith=username.replace('_',' ').replace('@',', '))
        ).distinct()

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Limit constituency choices depending on the user's username
        """
        if not request.user.is_superuser and not request.user.username.startswith('pr-'):
            user_prefix = request.user.username.upper()
            if db_field.name == "hor_constituency":
                kwargs['choices'] = [(None, '---')] + [
                    c for c in HoR_Constituency.choices if c[0].startswith(user_prefix)
                ]
            elif db_field.name == "province_constituency":
                kwargs['choices'] = [(None, '---')] + [
                    c for c in Province_Constituency.choices if c[0].startswith(user_prefix)
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "municipality" and not request.user.is_superuser:
            kwargs["queryset"] = Municipality.objects.annotate(
                full_display=Concat(
                    'name', 
                    Value(', '), 
                    'district__name',
                    output_field=CharField()
                )).filter(
                        Q(district__name__istartswith=request.user.username) |
                        Q(full_display__istartswith=request.user.username.replace('_',' ').replace('@',', '))
                    )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # hide proportional and order field from mods, as they are for PR.
    # hide hor_constituency and province_constituency from prmods as they are for FPTP.
    # check proportional field by default. require order field.
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.username.startswith('pr-'):
            for field_name, field in form.base_fields.items():
                if field_name in ['hor_constituency','province_constituency','municipality','local_position','ward']:
                    field.widget = forms.HiddenInput()
                if field_name == 'proportional':
                    field.initial = True
                    field.disabled = True
                if field_name in ['party','order']:
                    field.required = True
        elif not request.user.is_superuser:
            for field_name, field in form.base_fields.items():
                if field_name in ['proportional','order']:
                    field.widget = forms.HiddenInput()
        return form


    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
            return

        username = request.user.username

        if username.startswith('pr-'):
            party_code = int(username.split('-')[-1]) # extract party code from username
            if not obj.party:
                raise ValidationError('party field missing!')
            if obj.party.id != party_code:
                raise ValidationError('You are not allowed to set Representative for that party')
            if obj.hor_constituency or obj.province_constituency or obj.municipality:
                raise ValidationError('You aren\'t supposed to set constituency candidates')
            if not obj.order:
                raise ValidationError('order field missing!')

            super().save_model(request, obj, form, change)
            return

         # for FPTP mods, prevent changing proportional and order fields.

        for field in form.changed_data:
            if field in ['order','proportional']:
                raise ValidationError('You are not allowed to change these fields')

        user_prefix = username.upper()

        # if obj.hor_constituency.startswith(request.user.username) or obj.province_constituency.startswith(request.user.username):
        if not obj.hor_constituency and not obj.province_constituency and not obj.municipality:
            raise ValidationError('Must choose one constituency')
        if (obj.hor_constituency and obj.province_constituency) or (obj.hor_constituency and obj.municipality) or (obj.province_constituency and obj.municipality):
            raise ValidationError('Choose only one constituency')
        if (
            obj.hor_constituency
            and obj.hor_constituency.startswith(user_prefix)
        ) or (
            obj.province_constituency
            and obj.province_constituency.startswith(user_prefix)
        ) or (
            obj.municipality
            and obj.municipality.district.name.lower().startswith(username.lower())
        ) or (
            obj.municipality
            and obj.municipality.__str__().lower().startswith(username.replace('_',' ').replace('@',', ').lower())
        ):
            super().save_model(request, obj, form, change)
        else:             
            raise ValidationError('You are not allowed to set Representative of that constituency')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        username = request.user.username

        if not username.startswith('pr-'): return qs

        party_code = username.split('-')[-1]
        return qs.filter(id=party_code)

    def has_add_permission(self, request):
        if request.user.is_superuser: return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser: return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser: return True        
        return False

class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_np', 'district', 'wards')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs

        username = request.user.username
        return qs.annotate(
            full_display=Concat(
                'candidate__representative__municipality__name', 
                Value(', '), 
                'candidate__representative__municipality__district__name',
                output_field=CharField()
        )).filter(
            Q(district__name__istartswith=username) |
            Q(full_display__istartswith=request.user.username.replace('_',' ').replace('@',', '))
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False           


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_np')
    search_fields = ('name',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False           


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Kartut, KartutAdmin)
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(District, DistrictAdmin)
