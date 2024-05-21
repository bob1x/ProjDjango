from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import EvenementCreateView




urlpatterns = [
    
    # AUTHENTICATION
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.index, name="home"),
    
    # postes
    
    path("Myprofile/", views.poste_list, name="poste_list"),
    path("Myprofile/settings", views.profile_settings, name="profile_settings"),
    # path("poste/<int:pk>/", views.poste_detail, name="poste_detail"),
    path("post/<int:id>/edit/", views.poste_edit, name="poste_update"),
    path("post/<int:id>/delete/", views.poste_delete, name="poste_delete"),
    path("post/create/<str:type_p>/", views.poste_create, name="poste_create_dynamic"),
    path('post/about/<int:id>/', views.poste_details, name='poste_detail'),
    path('clear-notifications/', views.clear_notifications, name='clear_notifications'),
    path('post/<int:id>/delete ', views.poste_delete, name='delete_poste'),
    # path("poste/create/<str:post_type>/ ", PosteCreateView.as_view(), name="poste_create"),
    
    
    path('like/<int:post_id>/', views.like, name='like'),
    path('event/<int:event_id>/interested/', views.interested, name='interested'),

    # path('comment_poste/<int:id>/', comment_poste, name='comment_poste'),
   
    path('profile/<int:user_id>/', views.profile_user, name='profile'),
#    event 
    path('Myevents/', views.my_events, name='my_events'),
    path('event/', views.event_list, name='event_list'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('events/create/', EvenementCreateView.as_view(), name='create_event'),
    # path('event/<int:id>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:id>/delete/', views.event_delete, name='event_delete'),
    # path('event/<int:id>/edit/', views.event_edit, name='event_edit'),
    # path('event/<int:id>/delete/', views.event_delete, name='event_delete'),

#Friend rq 
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    
    path('accept_friend_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:friend_request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    
    
    # convo
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('create_message/<int:conversation_id>/', views.create_message, name='create_message'),  # Define the URL pattern for creating messages
    path('create-conversation/<int:user_id>/', views.create_conversation, name='create_conversation'),
# misc
    path('help/', views.help, name='Help')
    
]
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
