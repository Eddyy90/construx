from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils import timezone
from users.decorators import client_required
from .models import GroupProfile
from .forms import GroupProfileForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class GroupListView(PermissionRequiredMixin,ListView):
    permission_required = 'auth.view_group'
    model = GroupProfile
    paginate_by = 100
    context_object_name = 'groups'
    template_name = 'groups/index.html'

    def get_queryset(self):
        return GroupProfile.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class GroupCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.add_group'
    model = GroupProfile
    form_class = GroupProfileForm
    template_name = 'groups/form.html'
    success_url = reverse_lazy('groups:index')


class GroupDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.view_group'
    model = GroupProfile
    template_name = 'groups/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class GroupUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'
    model = GroupProfile
    form_class = GroupProfileForm
    template_name = 'groups/form.html'
    success_url = reverse_lazy('groups:index')


class GroupDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_group'
    model = GroupProfile
    template_name = 'groups/confirm_delete.html'
    success_url = reverse_lazy('groups:index')
