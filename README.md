## Candidates Profile Plaform: Nepal's Election

- Record candidates info of past and upcomming elections of all houses.

## Public Contribution

_Admin can create staff accounts with scoped permissions allowing users to either update candidates for certain constituency only or certain party only:_

- Username: `illam_1`: Can only update fptp candidates from illam-1 constituency
- Username: `illam` or `ill`: Can update fptp candidates from any of the constituency under illam or any  municipality under illam
- Username: `pr-xxx-3`: Can only update PR candidates of the party whose id is 3.  

### Setup for Self-host 

_Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS in `ramroneta/settings.py`_

- python3 manage.py collectstatic

- python3 manage.py makemigrations app

- python3 manage.py migrate

- python3 manage.py createsuperuser

- python3 manage.py loaddata district_fixtures

- python3 manage.py loaddata municipal_fixtures

## Run

- python3 manage.py runserver