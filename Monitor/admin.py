from django.contrib import admin
from ServerMonitor.Monitor.models import Account, CustomUser, Server, Monitor, Search, Socket, Message
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    list_display = ('company','owner',)

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','is_staff','last_login','account',)

class MonitorAdmin(admin.ModelAdmin):
    list_display = ('name','type','status','frequency','server',)

class MonitorInline(admin.TabularInline):
    model = Monitor

class ServerAdmin(admin.ModelAdmin):
    list_display = ('name','owner',)

    inlines = [MonitorInline,
              ]

class SearchAdmin(admin.ModelAdmin):
    list_display = ('monitor','address','type','value')

class SocketAdmin(admin.ModelAdmin):
    list_display = ('monitor','address','port')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('monitor','type','address')

admin.site.unregister(User)
admin.site.register(Account,AccountAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Monitor,MonitorAdmin)
admin.site.register(Server,ServerAdmin)
admin.site.register(Search,SearchAdmin)
admin.site.register(Socket,SocketAdmin)
admin.site.register(Message,MessageAdmin)
