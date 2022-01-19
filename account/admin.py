from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile,Relation


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendedProfileAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendedProfileAdmin)
admin.site.register(Relation)
