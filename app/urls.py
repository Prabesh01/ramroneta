from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('hor/<int:year>/', views.hor_home, name='hor_home'),
    path('hor/<int:year>/parties', views.hor_parties, name='hor_parties'),
    path('hor/<int:year>/constituencies', views.hor_constituencies, name='hor_constituencies'),
    path('hor/<int:year>/constituency/<str:constituency>/<int:candidate_id>', views.hor_fptp_candidate_detail, name='hor_fptp_candidate_detail'),
    path('hor/<int:year>/party/<str:party>/<int:candidate_id>', views.hor_pr_candidate_detail, name='hor_pr_candidate_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)