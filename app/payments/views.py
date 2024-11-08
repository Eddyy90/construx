from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.html import mark_safe

from .models import Payment
from payments.forms import PaymentForm


class PaymentListView(PermissionRequiredMixin, ListView):
    permission_required = 'payments.view_payment'
    model = Payment
    context_object_name = 'payments'
    template_name = 'payments/list.html'


class PaymentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'payments.add_payment'
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/form.html'
    success_url = reverse_lazy('payments:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if hasattr(self.object, 'created_by'):
            self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        message = mark_safe(f'Pagamento <strong>{self.object}</strong> criado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class PaymentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'payments.view_payment'
    model = Payment
    template_name = 'payments/detail.html'


class PaymentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'payments.change_payment'
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/form.html'
    success_url = reverse_lazy('payments:list')

    def form_valid(self, form):
        instance = form.save(commit=True)
        message = mark_safe(f'Pagamento <strong>{instance}</strong> editado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class PaymentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'payments.delete_payment'
    model = Payment
    template_name = 'payments/confirm_delete.html'
    success_url = reverse_lazy('payments:list')
