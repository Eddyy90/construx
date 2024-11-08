from address.forms import AddressForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from users.models import User
from users.decorators import client_required
from profiles.models import UserProfile, ClientProfile
from users.forms import ImpersonateForm, UserForm
from profiles.forms import (
    ClientProfileForm, UserProfileForm,
    WorkerCreationForm, WorkerForm
)


# @login_required
def login(request):
    if 'username' in request.session:
        return redirect('dashboard')
    else:
        return redirect('login')


# Dashboard
def index(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and user.is_client:
        # if ClientProfile is not fulfilled
        if not user.client_profile:
            return redirect('wizard')

    today = timezone.now()


    return render(request, 'misc/dashboard.html', {
        'users': UserProfile.objects.all(),
    })


def profile_detail(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and user.is_client:
        profile = user.client_profile
        if not profile:
            return redirect('wizard')
    else:
        profile = user.profile

    context = {
        'profile': profile,
    }

    return render(request, 'misc/profile.html', context)


def impersonate_profile(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and not user.is_superuser and not request.session['impersonate_id']:
        return redirect('dashboard')

    form = ImpersonateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        profile = form.cleaned_data['profile']
        if profile:
            user = User.objects.get(pk=profile.id)
            profile_email = user.email
            request.session['impersonate_id'] = int(user.id)
            request.user = user
            messages.info(request, f'Personificou usuário "{profile_email}" com sucesso!')
        else:
            del request.session['impersonate_id']
            messages.info(request, f'Despersonificou com sucesso!')
            if request.original_user:
                request.user = request.original_user

    context = {
        # 'profile': profile,
        'form': form,
    }

    return render(request, 'misc/impersonate_form.html', context)


def unimpersonate_profile(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and not user.is_superuser and not request.session['impersonate_id']:
        return redirect('dashboard')
    del request.session['impersonate_id']
    messages.info(request, f'Despersonificou com sucesso!')
    if request.original_user:
        request.user = request.original_user
    return redirect('profile_impersonate')


def edit_profile(request):
    if 'username' not in request.session:
        return redirect('login')
    user = request.user
    if user and user.is_client:
        profile = user.client_profile
        if not profile:
            return redirect('wizard')

    post_data = request.POST or None

    context = {}
    if user.is_client:
        profile = ClientProfile.objects.filter(user=user).first()
        user_form = UserForm(post_data, prefix='user_form', instance=user)
        if request.method == 'POST':
            profile_form = ClientProfileForm(post_data, request.FILES, prefix='profile_form', instance=profile)
        else:
            profile_form = ClientProfileForm(post_data, prefix='profile_form', instance=profile)
        profile_address_form = AddressForm(post_data, prefix='client_address_form', instance=profile.address)
        context = {
            'profile': profile,
            'client_form': user_form,
            'client_profile_form': profile_form,
            'client_address_form': profile_address_form,
        }
        validate_forms = [
            user_form, profile_form, profile_address_form
        ]
    elif user.is_user:
        profile = UserProfile.objects.filter(user=user).first()
        user_form = WorkerForm(
            post_data, prefix='user_form', instance=profile.user)
        if request.method == 'POST':
            user_profile_form = UserProfileForm(
                post_data, request.FILES, prefix='user_profile_form', instance=profile)
        else:
            user_profile_form = UserProfileForm(
                post_data, prefix='user_profile_form', instance=profile)
        context = {
            'profile': profile,
            'user_form': user_form,
            'user_profile_form': user_profile_form,
        }
        validate_forms = [user_form, user_profile_form]

    if request.method == 'POST':
        if all((f.is_valid() for f in validate_forms)):
            if user.is_client:
                if not profile.address:
                    profile.address = profile_address_form.save()

            for form in validate_forms:
                instance = form.save(commit=False)
                if isinstance(instance, UserProfile):
                    instance.user = user
                instance.save()

    return render(request, 'misc/edit_profile.html', context)


@client_required
@transaction.atomic
def wizard(request):
    # TODO test user on the first access to see if it has all the values like email
    user = request.user
    client_profile = ClientProfile.objects.filter(user=user).first()
    client_address = client_profile.address if client_profile else None
    client_form = UserForm(prefix='client_form', instance=user)
    client_profile_form = ClientProfileForm(prefix='client_profile_form', instance=client_profile)
    client_address_form = AddressForm(prefix='client_address_form', instance=client_address)
    user_form = WorkerCreationForm(prefix='user_form')
    user_profile_form = UserProfileForm(prefix='user_profile_form')
    step_index = 0

    if request.method == 'POST':
        form_id = request.POST.get('form_id')

        if form_id == 'client_form':
            client_form = UserForm(request.POST, prefix='client_form', instance=user)
            client_profile_form = ClientProfileForm(request.POST, prefix='client_profile_form', instance=client_profile)
            client_address_form = AddressForm(request.POST, prefix='client_address_form', instance=client_address)
            error = False
            if client_form.is_valid() and client_profile_form.is_valid():
                client_form.save()
                client_profile = client_profile_form.save(commit=False)
                client_profile.user_id = user.id
                if not client_profile.digital:
                    if client_address_form.is_valid():
                        client_profile.address = client_address_form.save()
                    else:
                        error = True
                client_profile.save()
            else:
                error = True

            if error:
                messages.error(request, f'Erro de validação ao atualizar perfil')
                messages.error(request, client_form.errors)
                messages.error(request, client_profile_form.errors)
                messages.error(request, client_address_form.errors)
            else:
                step_index = 1
                messages.success(request, f'Seu perfil foi atualizado com sucesso')
        elif form_id == 'user_form':
            user_form = WorkerCreationForm(request.POST, prefix='user_form')
            user_profile_form = UserProfileForm(request.POST, prefix='user_profile_form')
            step_index = 1
            if user_form.is_valid() and user_profile_form.is_valid():
                user = user_form.save(commit=False)
                user.type = User.Types.USER
                user.save()
                # TODO: Generate password and send through email
                # user.password = uuid()
                user.save()
                new_profile = user_profile_form.save(commit=False)
                new_profile.user_id = user.id
                new_profile.save()
                messages.success(request, f'Usuário com email {user.email} criado com sucesso')
                user_form = WorkerCreationForm(prefix='user_form')
                user_profile_form = UserProfileForm(prefix='user_profile_form')
            else:
                print('errors', user_form.errors)
                messages.error(request, f'Erro de validação ao criar usuário')

    return render(request, 'misc/wizard.html', {
        'client_profile': client_profile,
        'step_index': step_index,
        'client_form': client_form,
        'client_profile_form': client_profile_form,
        'client_address_form': client_address_form,
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'users': UserProfile.get_by_client(user).all()
    })


def support(request):
    return render(request, 'misc/support.html')
