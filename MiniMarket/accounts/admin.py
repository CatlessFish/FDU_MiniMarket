from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *
from .forms import *

# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm_super

    list_display = ('username', 'nickname', 'building_no',
        'room_no', 'contact', 'is_staff', )
    list_filter = ('is_staff',)

    fieldsets = (
        ('Basic info', {
            'fields': (
                'username', "password"
            ),
        }),
        ('Personal info', {
            'fields':(
                'date_of_birth', 'realname', 'workID', 'gender',
            ),
        }),
        ('Permissions', {
            'fields':(
                'is_worker',
            ),
        }),
    )

    add_fieldsets = (
        ('Basic info', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',),
        }),
        ('Personal info', {
            'classes': ('wide',),
            'fields': ('date_of_birth',  'workID', 'gender',),
        }),
        ('Permissions', {
            'fields':(
                'is_worker',
            ),
        })
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


# Register MyUser model
admin.site.register(SiteUser, UserAdmin)

# Unregister built-in permissions
admin.site.unregister(Group)