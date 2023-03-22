from django.contrib import admin
from core import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

# Register your models here.

# Customizing django admin as per the custom user model
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'username']

    fieldsets = (
        (
            None,  # Here title is 'None'
            {
                "fields": ('email', 'password')
            }
        ),
        (
            _('Personal Info'),
            {
                "fields": ('name',)
            }
        ),
        (
            _('Permissions'),
            {
                "fields": ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important dates'),
            {
                "fields": ('last_login',)
            }
        )
    )


    # To modify Create/Add new user page in django admin
    add_fieldsets = (
        (None, {
            # 'classes' To add custom css classes.
            # ('wide') class to make the field wide
            # in new user django admin page.
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.File)