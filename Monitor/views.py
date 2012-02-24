from ServerMonitor.Monitor.models import Account, CustomUser, Server, Monitor, Search, Socket, Message
from ServerMonitor.Monitor.forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as log_in, logout as log_out, authenticate
from django.contrib.auth.decorators import login_required

def main(request):
    if request.user.is_authenticated():
        servers = Server.objects.filter(owner=request.user.account)
        return render_to_response('monitor/index.html',
                                {'servers':servers,},
                                context_instance=RequestContext(request))
    return render_to_response('monitor/index.html',
                             {'form':AuthenticationForm(request),},
                             context_instance=RequestContext(request))

@login_required
def add_server(request):
    if request.method == "POST":
        form = AddServerForm({'name':request.POST['name']})
        if form.is_valid():
            name = form.cleaned_data['name']
            owner = request.user.account
            try:
                new_server = Server.objects.get(name=name, owner=owner)
            except Server.DoesNotExist:
                new_server = Server.objects.create(name=name, owner=owner, level=0)
            else:
                return render_to_response('monitor/add-server.html',
                                          {'error':'It seems this server already exists!',
                                           'form':form,},
                                           context_instance=RequestContext(request))
            return HttpResponseRedirect(reverse('main_page'))
        else:
            return render_to_response('monitor/add-server.html',
                                      {'error':'Please give the server a name!',
                                       'form':form,},
                                       context_instance=RequestContext(request))

    form = AddServerForm()
    return render_to_response('monitor/add-server.html',
                             {'form':form,},
                             context_instance=RequestContext(request))

def edit_server(request, id):
    try:
        thisServer = Server.objects.get(pk=id)
    except Server.DoesNotExist:
        return HttpResponseRedirect(reverse('add-server'))
    else:
        if request.method == "POST":
            form = AddServerForm({'name':request.POST['name']})
            if form.is_valid():
                thisServer = Server.objects.get(pk=id)
                name = form.cleaned_data['name']
                owner = thisServer.owner
                if request.user.account == thisServer.owner:
                    try:
                        new_server = Server.objects.get(name=name, owner=owner)
                    except Server.DoesNotExist:
                        thisServer.name = name
                        thisServer.save()
                    else:
                        return render_to_response('monitor/edit-server.html',
                                                  {'error':'It seems this server already exists!',
                                                   'form':form,
                                                   'server':thisServer,},
                                                   context_instance=RequestContext(request))

                    return HttpResponseRedirect(reverse('main_page'))
                else:
                    return render_to_response('monitor/edit-server.html',
                                             {'error':'This server is not associated with your account',
                                              'form':form,
                                              'server':thisServer,},
                                              context_instance=RequestContext(request))
            else:
                return render_to_response('monitor/edit-server.html',
                                          {'error':'Please give the server a name!',
                                           'form':form,
                                           'server':thisServer,},
                                           context_instance=RequestContext(request))

    form = AddServerForm({'name':thisServer.name})
    return render_to_response('monitor/edit-server.html',
                             {'form':form,
                              'server':thisServer,},
                             context_instance=RequestContext(request))

@login_required
def view_monitors(request, id):
    try:
        thisServer = Server.objects.get(pk=id)
    except Server.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page'))
    else:
        if thisServer.owner == request.user.account:
            monitors = Monitor.objects.filter(server=thisServer)
            return render_to_response('monitor/view-monitors.html',
                                     {'monitors':monitors,'server':thisServer},
                                     context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(reverse('main_page'))

def add_monitor(request,id):
    try:
        thisServer = Server.ojects.get(pk=id)
    except Server.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page'))
    else:
        if thisServer.owner == request.user.account:
            if request.method == "POST":
                form = AddMonitorForm({'name':request.POST['name'],
                                       'type':request.POST['type'],
                                       'status':request.POST['status'],
                                       'frequency':request.POST['frequency'],
                                       'server':thisServer})
                if form.is_valid():
                    name = form.cleaned_data['name']
                    type = form.cleaned_data['type']
                    status = form.cleaned_data['status']
                    frequency = form.cleaned_data['frequency']
                    server = thisServer
                    try:
                        monitor = Monitor.objects.get(name=name, type=type, frequency=frequency, server=server)
                    except Monitor.DoesNotExist:
                        monitor = Monitor(name=name, type=type, frequency=frequency, server=server)
                        monitor.save()
                        return HttpResponseRedirect(reverse('view-monitors',server.id))
                    else:

                else:
                    return render_to_reponse('monitor/add-monitor.html',
                                            {'form':form,},
                                            context_instance=RequestContext(request))
            else:
                form = AddMonitorForm()
                return render_to_response('monitor/add-monitor.html',
                                         {'form':form,},
                                         context_instance=RequestContet(request))
    return HttpResponseRedirect(reverse('view-monitors',server.id))



@login_required
def view_messages(request, id):
    thisMonitor = Monitor.objects.get(pk=id)
    messages = Message.objects.filter(monitor=thisMonitor)
    return render_to_response('monitor/view-messages.html',
                             {'messages':messages,'server':thisMonitor.server,'monitor':thisMonitor},
                             context_instance=RequestContext(request))

@login_required
def edit_message(request, id):
    thisMessage = Message.objects.get(pk=id)
    return HttpResponse(thisMessage)

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                log_in(request, user)
                
                try:
                    return HttpResponseRedirect(request.POST['next'])
                except:
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

@login_required
def logout(request):
    log_out(request)
    return HttpResponseRedirect(reverse('main_page'))
