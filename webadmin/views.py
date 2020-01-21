from django.shortcuts import render, redirect
from .models import HostGroup, Module, Host, Argument
from .adhoc2 import adhoc
import os


# Create your views here.
def host_info(request):
    return render(request, "host_info.html")


def add_hosts(request):
    if request.method == "POST":
        groupname = request.POST.get('group')
        hostname = request.POST.get('host')
        ip_addr = request.POST.get('ip')
        collect = request.POST.get('collect')
        if groupname:
            group = HostGroup.objects.get_or_create(groupname=groupname)[0]
            if hostname and ip_addr:
                group.host_set.get_or_create(hostname=hostname, ip_addr=ip_addr)
        if collect == "True":
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ansi_cfg_dir = os.path.join(project_dir, "ansi_cfg")
            script_path = os.path.join(ansi_cfg_dir, "hosts_cmdb")
            os.system("%s %s" % (script_path, ansi_cfg_dir))

    groups = HostGroup.objects.all()
    return render(request, "add_hosts.html", {'groups': groups})


def add_modules(request):
    if request.method == 'POST':
        modulename = request.POST.get('module')
        arg_text = request.POST.get('args')
        if modulename:
            module = Module.objects.get_or_create(modulename=modulename)[0]
            if arg_text:
                module.argument_set.get_or_create(arg_text=arg_text)
    modules = Module.objects.all()
    return render(request, "add_modules.html", {'modules': modules})


def result(request):
    if request.method == 'POST':
        ip = request.POST.get('host_selected')
        group = request.POST.get('group_selected')
        module = request.POST.get('module_selected')
        args = request.POST.get('args_selected')
        dest = None
        if ip:
            dest = ip
        elif group:
            dest = group
        if dest and module and args:
            adhoc(['ansi_cfg/dhosts.py'], dest, module, args)
        return render(request, "result.html")


def tasks(request):
    hosts = Host.objects.all()
    groups = HostGroup.objects.all()
    modules = Module.objects.all()
    context = {'groups': groups, 'hosts': hosts, 'modules': modules}
    return render(request, "tasks.html", context)


def del_arg(request, pk_id, flag):
    if flag == "1":
        host = Host.objects.get(id=pk_id)
        host.delete()
        return redirect('add_hosts')
    elif flag == "2":
        group = HostGroup.objects.get(id=pk_id)
        group.host_set.all().delete()
        group.delete()
        return redirect('add_hosts')
    elif flag == "3":
        arg = Argument.objects.get(id=pk_id)
        arg.delete()
        return redirect('add_modules')
    elif flag == "4":
        module = Module.objects.get(id=pk_id)
        module.argument_set.all().delete()
        module.delete()
        return redirect('add_modules')
