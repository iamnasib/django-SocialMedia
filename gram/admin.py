from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SignupForm, MyUserChangeForm
from .models import MyUser,Posts,Comments,Like,Tales,IsSaved

class MyUserAdmin(UserAdmin):
    add_form = SignupForm
    form = MyUserChangeForm
    model = MyUser
    list_display = ['username', 'mobile_number', 'full_name','email','is_deactivated','website',]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('mobile_number', 'full_name','DOB','is_deactivated','is_verified','is_private','bio','website',
            'DP','followers','requested_to','gender','blocked_user')}),
    ) #this will allow to change these fields in admin module


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Like)
admin.site.register(Tales)
admin.site.register(IsSaved)