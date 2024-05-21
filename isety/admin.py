from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Poste, Recommandation, Message,Conversation,Transport, Logement, Stage,FriendRequest , Likes,Comment,Notification, Evenement, Intrested,Archives
from django.contrib.auth.models import Group

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'photo', 'telnum', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'photo', 'telnum')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',), 
            'fields': (
                'email', 'first_name', 'last_name', 'photo', 'telnum',
                'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions',
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Poste)
admin.site.register(Recommandation)
admin.site.register(Transport)
admin.site.register(Logement)
admin.site.register(Stage)
admin.site.register(Evenement)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Intrested)
admin.site.register(FriendRequest)
admin.site.register(Conversation)
admin.site.register(Message)
# Unregister the Group model from admin since we are using a custom User model
admin.site.unregister(Group)
admin.site.register(Archives)