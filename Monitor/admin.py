from django.contrib import admin
from ServerMonitor.Monitor.models import Account, CustomUser, Server, Monitor, Search, Socket, Message
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    list_display = ('company','owner',)

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','is_staff','last_login','account',)

class MonitorInline(admin.TabularInline):
    model = Monitor

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name','owner',)

    inlines = [MonitorInline,
              ]

admin.site.unregister(User)
admin.site.register(Account,AccountAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Server,ServerAdmin)
