from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import mark_safe

from .models import Notification
from user_notifications.forms import NotificationForm


class NotificationListView(PermissionRequiredMixin, ListView):
    permission_required = 'user_notifications.view_usernotification'
    model = Notification
    context_object_name = 'user_notifications'
    template_name = 'user_notifications/list.html'


class NotificationTimelineView(PermissionRequiredMixin, ListView):
    permission_required = 'user_notifications.view_usernotification'
    model = Notification
    context_object_name = 'notifications'
    template_name = 'user_notifications/timeline.html'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(recipient=user)


class NotificationCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'user_notifications.add_usernotification'
    model = Notification
    form_class = NotificationForm
    template_name = 'user_notifications/form.html'
    success_url = reverse_lazy('user_notifications:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if hasattr(self.object, 'created_by'):
            self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        message = mark_safe(f'Notificação de Usuário <strong>{self.object}</strong> criado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class NotificationDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'user_notifications.view_usernotification'
    model = Notification
    template_name = 'user_notifications/detail.html'


class NotificationUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'user_notifications.change_usernotification'
    model = Notification
    form_class = NotificationForm
    template_name = 'user_notifications/form.html'
    success_url = reverse_lazy('user_notifications:list')

    def form_valid(self, form):
        instance = form.save(commit=True)
        message = mark_safe(f'Notificação de Usuário <strong>{instance}</strong> editado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class NotificationDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'user_notifications.delete_usernotification'
    model = Notification
    template_name = 'user_notifications/confirm_delete.html'
    success_url = reverse_lazy('user_notifications:list')
