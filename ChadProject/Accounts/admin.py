from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


User = get_user_model()

#  if your user model extends AbstractBaseUser, you’ll need to define a custom ModelAdmin class. It may be possible to subclass the default django.contrib.auth.admin.UserAdmin; however, you’ll need to override any of the definitions that refer to fields on django.contrib.auth.models.AbstractUser that aren’t on your custom user class.

# src : https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    # list_display = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal Info'), {'fields': (
            'first_name', 'last_name', 'gender', 'phone_number', 'bio', 'followers', 'profile_picture',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_admin',)}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'phone_number', 'bio', 'followers', 'profile_picture', 'is_active', 'is_staff', 'is_superuser', 'is_admin',)
        }),
    )
    filter_horizontal = ('followers',)


admin.site.register(User, UserAdmin)
