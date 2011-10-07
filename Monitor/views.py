from ServerMonitor.Monitor.models import Account, CustomUser, Server, Monitor, Search, Socket, Message
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as log_in, logout as log_out, authenticate

def main(request):
    if request.user.is_authenticated():
        servers = Server.objects.filter(owner=request.user.account)
        return render_to_response('monitor/index.html',
                                {'servers':servers,},
                                context_instance=RequestContext(request))
    return render_to_response('monitor/index.html',
                             {'form':AuthenticationForm(request),},
                             context_instance=RequestContext(request))
def edit_server(request, id):
    thisServer = Server.objects.get(pk=id)
    monitors = Monitor.objects.filter(server=thisServer)
    return render_to_response('monitor/edit-server.html',
                             {'monitors':monitors},
                             context_instance=RequestContext(request))

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                log_in(request, user)
                return HttpResponseRedirect(reverse('main_page'))
            else:
                return render_to_response('monitor/login.html',
                                         {'form':AuthenticationForm(request),'error':'It appears that your account is currently disabled.  Please email the admin to figure out why.'},
                                         context_instance=RequestContext(request))
        else:
            return render_to_response('monitor/login.html',
                                     {'form':AuthenticationForm(request),'error':'Your login information seems to be incorrect.  Try correcting this and login again.'},
                                     context_instance=RequestContext(request))
    else:
        return render_to_response('monitor/login.html',
                                 {'form':AuthenticationForm(request)},
                                 context_instance=RequestContext(request))

def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('main_page'))
