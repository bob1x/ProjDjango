from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    # AUTHENTICATION
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.index, name="home"),
    
    # postes
    
    path("poste/", views.poste_list, name="poste_list"),
    # path("poste/<int:pk>/", views.poste_detail, name="poste_detail"),
    path("poste/<int:id>/edit/", views.poste_edit, name="poste_update"),
    path("poste/<int:id>/delete/", views.poste_delete, name="poste_delete"),
    path("poste/create/<str:post_type>/", views.poste_create, name="poste_create_dynamic"),
    path("poste/details/<int:id>/", views.poste_details, name="poste_details"),
    
    # path("poste/create/<str:post_type>/ ", PosteCreateView.as_view(), name="poste_create"),
    

]
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
