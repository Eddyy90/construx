from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .forms import ClientSettingsForm
from django.conf import settings
from django.db import utils
from django.views.generic import TemplateView
from django_tenants.utils import tenant_context, remove_www

from clients.models import Client
from clients.forms import DomainForm
from clients import lib
from users.decorators import admin_required, client_required
from misc import views as base_views



def index(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if not user or not user.is_authenticated:
        return redirect('login')
    if user.is_admin:
        return redirect('clients:index')
    if user.is_client:
        return redirect('dashboard')
    if user.is_user:
        return redirect('profile_edit')


def dashboard(request):
    tenant = Client.objects.filter(user=request.user).first()
    if not tenant:
        return redirect('setup')
    with tenant_context(tenant):
        # user = tenant.get_client_user()
        if request.user.is_authenticated:
            print('>>> request session', request.session)
        # auth.login(request, user)
        scheme_url = request.is_secure() and "https" or "http"
        url = f"{scheme_url}://{tenant.get_primary_domain()}"
        response = HttpResponseRedirect(url)
        return response


def setup(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and not user.is_client:
        return redirect('index')
    tenant = Client.objects.filter(user=user)
    if tenant:
        return redirect('dashboard')

    form = DomainForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        domain_url = form.cleaned_data['domain']
        tenant = lib.create_user_tenant(user, domain_url)
        lib.setup_user_tenant(tenant)
        messages.info(request, f'Tenant criado com sucesso')
        return redirect('dashboard')

    context = {
        'form': form,
    }

    return render(request, 'clients/setup_form.html', context)


class ClientsView(TemplateView):
    template_name = 'clients/index.html'

    # @admin_required
    # def dispatch(self, *args, **kwargs):
    #     return super(ClientsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)

        hostname_without_port = remove_www(self.request.get_host().split(':')[0])

        try:
            Client.objects.get(schema_name='public')
        except utils.DatabaseError:
            context['need_sync'] = True
            context['shared_apps'] = settings.SHARED_APPS
            context['tenants_list'] = []
            return context
        except Client.DoesNotExist:
            context['no_public_tenant'] = True
            context['hostname'] = hostname_without_port

        if Client.objects.count() == 1:
            context['only_public_tenant'] = True

        context['tenants_list'] = Client.objects.all()
        return context


@admin_required
def client_detail(request, pk):
    tenant = Client.objects.get(pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        with tenant_context(tenant):
            messages.error(request, f'Nothing to do here ;)')

    context = {
        # 'form': form,
        'object': tenant,
    }
    return render(request, 'clients/detail.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def root_edit_settings(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return _edit_setting(request, client)


@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def edit_settings(request):
    client = request.tenant
    return _edit_setting(request, client)


def _edit_setting(request, client):
    try:
        client_settings = client.settings
    except ObjectDoesNotExist:
        client_settings = None

    if request.method == 'POST':
        form = ClientSettingsForm(request.POST, request.FILES, instance=client_settings)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client_id = client.id
            instance.save()
            messages.success(request, 'Imagem alterada com sucesso!')
            return redirect('dashboard')
    else:
        form = ClientSettingsForm(instance=client_settings)

    return render(
        request,
        'clients/edit_settings.html',
        {'form': form, 'client_profile': client_settings},
    )
