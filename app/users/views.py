from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from users.models import User
from users.decorators import client_required
from profiles.models import UserProfile
from profiles.forms import UserProfileForm, WorkerCreationForm, WorkerForm
from django.contrib.auth.decorators import permission_required



@permission_required('users.view_user')
def index(request):
    user = request.user
    users_list = UserProfile.objects.all()
    context = {'user_profiles_list': users_list}
    return render(request, 'users/index.html', context)


@permission_required('users.add_user')
def create(request):
    # client_user = request.user
    # profile = ClientProfile.objects.filter(user=client_user).first()
    user_form = WorkerCreationForm(
        request.POST or None, prefix='user_form')
    user_profile_form = UserProfileForm(
        request.POST or None, prefix='user_profile_form')

    if request.method == 'POST':
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
            return redirect('users:edit', user.id)
        else:
            messages.error(request, f'Erro de validação ao criar usuário')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'users/form.html', context)


@permission_required('users.change_user')
def edit(request, pk):
    profile_user = User.objects.filter(pk=pk).first()
    profile = UserProfile.objects.filter(user=profile_user).first()
    user_form = WorkerForm(
        request.POST or None, prefix='user_form', instance=profile.user)
    user_profile_form = UserProfileForm(
        request.POST or None, prefix='user_profile_form', instance=profile)

    if request.method == 'POST':
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            user_profile_form.save()
            messages.success(request, f'Usuário com email {user.email} atualizado com sucesso')
        else:
            messages.error(request, f'Erro de validação ao atualizar usuário')

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'users/form.html', context)


@permission_required('users.view_user')
def detail(request, pk):
    profile_user = User.objects.filter(pk=pk).first()
    if profile_user.is_user:
        profile = UserProfile.objects.filter(user=profile_user).first()

    context = {
        'profile': profile,
    }

    return render(request, 'misc/profile.html', context)
