from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import mark_safe

from .models import Animal
from animals.forms import AnimalForm


class AnimalListView(PermissionRequiredMixin, ListView):
    permission_required = 'animals.view_animal'
    model = Animal
    context_object_name = 'animals'
    template_name = 'animals/list.html'


class AnimalCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'animals.add_animal'
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/form.html'
    success_url = reverse_lazy('animals:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if hasattr(self.object, 'created_by'):
            self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        message = mark_safe(f'Animal <strong>{self.object}</strong> criado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class AnimalDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'animals.view_animal'
    model = Animal
    template_name = 'animals/detail.html'


class AnimalUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'animals.change_animal'
    model = Animal
    form_class = AnimalForm
    template_name = 'animals/form.html'
    success_url = reverse_lazy('animals:list')

    def form_valid(self, form):
        instance = form.save(commit=True)
        message = mark_safe(f'Animal <strong>{instance}</strong> editado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class AnimalDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'animals.delete_animal'
    model = Animal
    template_name = 'animals/confirm_delete.html'
    success_url = reverse_lazy('animals:list')
