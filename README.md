## Candidates Profile Plaform: Nepal's Election

- Record candidates info of past and upcomming elections of all houses.

## Public Contribution

_Admin can create staff accounts with scoped permissions allowing users to either update candidates for certain constituency only or certain party only:_

- Username: `illam_1`: Can only update fptp candidates from illam-1 constituency [Hor and Province House].
- Username: `illam` or `illa` or `ill`: Can update fptp candidates from any of the constituencies under illam  [Hor and Province House]. Can also update candidates of any municipality under illam [Local Level].
- Username: `pr-xxx-3`: Can only update PR candidates of the party whose id is 3 [Hor and Province House].
- Username: `Miklajung_Rural_Municipality@Mor`: Can only update candidates of Miklajung rural municipality of Morang district and all of its wards [Local Level].

> Since there are only limited number of parties and very few members in National Assembly, admin can add these themself manually; no specific mod access is setup for their contribution. 

### Setup for Self-host 

_Copy `.env.example` to `.env` and Update ALLOWED_HOSTS & CSRF_TRUSTED_ORIGINS in `ramroneta/settings.py`_

- python3 manage.py collectstatic

- python3 manage.py makemigrations app

- python3 manage.py migrate

- python3 manage.py createsuperuser

- python3 manage.py loaddata district_fixtures

- python3 manage.py loaddata municipal_fixtures

## Run

- python3 manage.py runserver

- For comment feature, edit isso.cfg file and script src in `app/templates/candidates.html` and then run: isso -c isso.cfg run
