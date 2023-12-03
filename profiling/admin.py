from django.contrib import admin
from .models import UserProfile, Role, NextOfKin, Bank
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(NextOfKin)
admin.site.register(Bank)