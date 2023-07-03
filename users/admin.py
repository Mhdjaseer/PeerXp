from django.contrib import admin
from .models import CustomUser,Department,Ticket

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Ticket)