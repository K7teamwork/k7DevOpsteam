# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # URL for the register view
    path('login/', views.login, name='login'),  # URL for the login view
    path('logout/', views.logout, name='logout'),  # URL for the logout view
    path('dashboard/', views.dashboard, name='dashboard'),  # URL for the dashboard view
    path('vote_page/', views.vote_page, name='vote_page'),  # URL for the vote view
    path('vote/<int:candidate_id>/', views.vote, name='vote'),  # URL for the vote view
    path('results/', views.results, name='results'),  # URL for the results view
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]