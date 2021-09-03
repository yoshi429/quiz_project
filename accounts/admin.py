from django.contrib import admin

from .models import User, ContactUs, Profile

admin.site.register(User)
admin.site.register(ContactUs)
admin.site.register(Profile)
