import datetime
from django.utils.dateparse import parse_datetime

import pytz

from django.conf import settings
from django.views.decorators.http import require_POST
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, F

from django.utils.html import mark_safe
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)
from schedule.forms import EventForm, OccurrenceForm
from schedule.models import Calendar, Event, Occurrence
from schedule.periods import weekday_names


from schedule.utils import (
    check_calendar_permissions,
    check_event_permissions,
    check_occurrence_permissions,
    coerce_date_dict,
)

from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Event, Calendar, Occurrence, get_object_calendar
from .forms import EventForm


class EventListView(PermissionRequiredMixin, ListView):
    permission_required = 'calendars.view_event'
    model = Event
    context_object_name = 'calendars'
    template_name = 'calendars/list.html'


class EventCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'calendars.add_event'
    model = Event
    form_class = EventForm
    template_name = 'calendars/form.html'
    success_url = reverse_lazy('calendars:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if hasattr(self.object, 'creator'):
            self.object.creator = self.request.user
            self.object.calendar = get_object_calendar(self.request.user)
            self.object.save()
        form.save_m2m()
        message = mark_safe(f'Evento <strong>{self.object}</strong> criado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class EventDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'calendars.view_event'
    model = Event
    template_name = 'calendars/detail.html'


class EventUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'calendars.change_event'
    model = Event
    form_class = EventForm
    template_name = 'calendars/form.html'
    success_url = reverse_lazy('calendars:list')

    def form_valid(self, form):
        instance = form.save(commit=True)
        message = mark_safe(f'Evento <strong>{instance}</strong> editado com sucesso')
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Houve problema na validação do formulário')
        if (form_errors := form.non_field_errors()):
            for error in form_errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class EventDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'calendars.delete_event'
    model = Event
    template_name = 'calendars/confirm_delete.html'
    success_url = reverse_lazy('calendars:list')


class FullCalendarView(PermissionRequiredMixin, ListView):
    permission_required = 'calendars.view_event'
    model = Event
    template_name = "calendars/fullcalendar.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar = get_object_calendar(self.request.user)
        form_modal = EventForm()
        context["calendar_slug"] = calendar.slug
        context["form_modal"] = form_modal
        return context


def event_detail_modal(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}

    return render(request, "calendars/ajax_detail_modal.html", context)


def event_edit_modal(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("calendars:fullcalendar")
    else:
        form = EventForm(instance=event)
        context["form"] = form

    return render(request, "calendars/ajax_edit_modal.html", context)


@check_calendar_permissions
@require_POST
def api_move_or_resize_by_code(request):
    response_data = {}
    user = request.user
    id = request.POST.get("id")
    existed = bool(request.POST.get("existed") == "true")
    delta = datetime.timedelta(minutes=int(request.POST.get("delta")))
    resize = bool(request.POST.get("resize", False))
    event_id = request.POST.get("event_id")

    response_data = _api_move_or_resize_by_code(
        user, id, existed, delta, resize, event_id
    )

    return JsonResponse(response_data)


def _api_move_or_resize_by_code(user, id, existed, delta, resize, event_id):
    response_data = {}
    response_data["status"] = "PERMISSION DENIED"

    if existed:
        occurrence = Occurrence.objects.get(id=id)
        occurrence.end += delta
        if not resize:
            occurrence.start += delta
        if user.has_perm('schedule.change_occurrence', occurrence):
            occurrence.save()
            response_data["status"] = "OK"
    else:
        event = Event.objects.get(id=event_id)
        dts = 0
        dte = delta
        if not resize:
            event.start += delta
            dts = delta
        event.end = event.end + delta
        if user.has_perm('schedule.change_event', event):
            event.save()
            event.occurrence_set.all().update(
                original_start=F("original_start") + dts,
                original_end=F("original_end") + dte,
            )
            response_data["status"] = "OK"
    return response_data


@check_calendar_permissions
def api_occurrences(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    calendar_slug = request.GET.get("calendar_slug")
    timezone = request.GET.get("timezone")

    try:
        response_data = _api_occurrences(start, end, calendar_slug, timezone)
    except (ValueError, Calendar.DoesNotExist) as e:
        return HttpResponseBadRequest(e)

    return JsonResponse(response_data, safe=False)


def _api_occurrences(start, end, calendar_slug, timezone):

    if not start or not end:
        raise ValueError("Start and end parameters are required")

    # version 2 of full calendar
    # TODO: improve this code with date util package
    if "-" in start:

        def convert(ddatetime):
            if ddatetime:
                ddatetime = ddatetime.split(" ")[0]
                try:
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%d")
                except ValueError:
                    # try a different date string format first before failing
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%dT%H:%M:%S")

    else:

        def convert(ddatetime):
            return datetime.datetime.utcfromtimestamp(float(ddatetime))

    start = convert(start.rsplit('Z')[0])
    end = convert(end.rsplit('Z')[0])
    current_tz = False
    if timezone and timezone in pytz.common_timezones:
        # make start and end dates aware in given timezone
        current_tz = pytz.timezone(timezone)
        start = current_tz.localize(start)
        end = current_tz.localize(end)
    elif settings.USE_TZ:
        # If USE_TZ is True, make start and end dates aware in UTC timezone
        utc = pytz.UTC
        start = utc.localize(start)
        end = utc.localize(end)

    if calendar_slug:
        # will raise DoesNotExist exception if no match
        calendars = [Calendar.objects.get(slug=calendar_slug)]
    # if no calendar slug is given, get all the calendars
    else:
        calendars = Calendar.objects.all()
    response_data = []
    # Algorithm to get an id for the occurrences in fullcalendar (NOT THE SAME
    # AS IN THE DB) which are always unique.
    # Fullcalendar thinks that all their "events" with the same "event.id" in
    # their system are the same object, because it's not really built around
    # the idea of events (generators)
    # and occurrences (their events).
    # Check the "persisted" boolean value that tells it whether to change the
    # event, using the "event_id" or the occurrence with the specified "id".
    # for more info https://github.com/llazzaro/django-scheduler/pull/169
    i = 1
    if Occurrence.objects.all().exists():
        i = Occurrence.objects.latest("id").id + 1
    event_list = []
    for calendar in calendars:
        # create flat list of events from each calendar
        event_list += calendar.events.filter(start__lte=end).filter(
            Q(end_recurring_period__gte=start) | Q(end_recurring_period__isnull=True)
        )
    for event in event_list:
        occurrences = event.get_occurrences(start, end)
        for occurrence in occurrences:
            occurrence_id = i + occurrence.event.id
            existed = False

            if occurrence.id:
                occurrence_id = occurrence.id
                existed = True

            recur_rule = occurrence.event.rule.name if occurrence.event.rule else None

            if occurrence.event.end_recurring_period:
                recur_period_end = occurrence.event.end_recurring_period
                if current_tz:
                    # make recur_period_end aware in given timezone
                    recur_period_end = recur_period_end.astimezone(current_tz)
                recur_period_end = recur_period_end
            else:
                recur_period_end = None

            event_start = occurrence.start
            event_end = occurrence.end
            if current_tz:
                # make event start and end dates aware in given timezone
                event_start = event_start.astimezone(current_tz)
                event_end = event_end.astimezone(current_tz)
            if occurrence.cancelled:
                # fixes bug 508
                continue
            response_data.append(
                {
                    "can_edit": True,
                    "id": occurrence_id,
                    "title": occurrence.title,
                    "link": event.get_absolute_url(),
                    "start": event_start,
                    "end": event_end,
                    "existed": existed,
                    "event_id": occurrence.event.id,
                    "color": occurrence.event.color_event,
                    "description": occurrence.description,
                    "rule": recur_rule,
                    "end_recurring_period": recur_period_end,
                    "creator": str(occurrence.event.creator),
                    "calendar": occurrence.event.calendar.slug,
                    "cancelled": occurrence.cancelled,
                }
            )

    return response_data