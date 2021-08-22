from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Tutor

admin.site.register(Tutor, UserAdmin)
