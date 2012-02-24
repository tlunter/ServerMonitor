from django import template
from ServerMonitor.Monitor.models import Monitor, Search, Socket

register = template.Library()

@register.filter
def searches(value):
   return Search.objects.filter(monitor=value) 

@register.filter
def sockets(value):
   return Socket.objects.filter(monitor=value) 
