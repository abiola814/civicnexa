from django.contrib import admin
from .models import Profile, Role, NextOfKin, Relatives
# Register your models here.


admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(NextOfKin)
admin.site.register(Relatives)

