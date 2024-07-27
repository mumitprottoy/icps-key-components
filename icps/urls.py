from django.contrib import admin
from django.urls import path
from home import views as home_views
from entrance import views as entrance_views
from profiles import views as profiles_views
from teams import views as team_views
from stats import views as stat_views

urlpatterns = [
    path('mnbvcxz/', admin.site.urls, name='backdoor'),
    path('', home_views.home, name='home'),
    path('nope/', home_views.nope, name='nope'),
    path('logout/', home_views.signout, name='logout'),
    path('signup/', entrance_views.signup, name='signup'),
    path('login/', entrance_views.signin, name='login'),
    path('activate/<str:link>', entrance_views.acivate_account, name='activate'),
    path('magic/<str:link>', entrance_views.magic_link, name='magic'),
    path('forgot-password/', entrance_views.forgot_password, name='forgot-password'),
    path('change-password/', profiles_views.change_password, name='change-password'),
    path('set-profile-picture/', profiles_views.set_profile_picture, name='set-profile-picture'),
    path('set-kit-name-and-number/', profiles_views.set_kit_name_and_number, name='set-kit-name-and-number'),
    path('set-captain/', team_views.set_captain, name='set-captain'),
    path('profile/<str:username>', profiles_views.user_profile, name='profile'),
    path('teams/<str:team>', profiles_views.team_profile, name='team-profile'),
    path('teams/squad-full', team_views.squad_full, name='squad-full'),
    path('teams/squad/<str:team>', team_views.list_squad, name='squad'),
    path('join-requests/<str:team>', team_views.list_join_requests, name='join-requests'),
    path('join-club/', team_views.join_club, name='join-club'),
    path('leave-club/<str:team>', team_views.leave_club, name='leave-club'),
    path('delete-join-request/', team_views.delete_join_request, name='delete-join-request'),
    path('approve-join-request/<int:join_id>', team_views.approve_join_request, name='approve-join-request'),
    path('reject-join-request/<int:join_id>', team_views.reject_join_request, name='reject-join-request'),
    path('fixtures/', stat_views.list_fixtures, name='fixtures')
]
