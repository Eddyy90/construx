from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import mark_safe

from .models import Work
from works.forms import WorkForm


class WorkListView(PermissionRequiredMixin, ListView):
    permission_required = 'works.view_work'
    model = Work
    context_object_name = 'works'
    template_name = 'works/list.html'


class WorkCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'works.add_work'
    model = Work
    form_class = WorkForm
    template_name = 'works/form.html'
    success_url = reverse_lazy('works:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if hasattr(self.object, 'created_by'):
            self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        message = mark_safe(f'Obra <strong>{self.object}</strong> criado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class WorkDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'works.view_work'
    model = Work
    template_name = 'works/detail.html'


class WorkUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'works.change_work'
    model = Work
    form_class = WorkForm
    template_name = 'works/form.html'
    success_url = reverse_lazy('works:list')

    def form_valid(self, form):
        instance = form.save(commit=True)
        message = mark_safe(f'Obra <strong>{instance}</strong> editado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class WorkDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'works.delete_work'
    model = Work
    template_name = 'works/confirm_delete.html'
    success_url = reverse_lazy('works:list')
