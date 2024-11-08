from schedule.models import Event, Calendar, CalendarRelation, Occurrence
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify



def get_object_calendar(object):
    calendar = None
    relation = CalendarRelation.objects.filter(
        object_id=object.pk,
        content_type=ContentType.objects.get_for_model(object)
    ).first()

    if relation:
        calendar = relation.calendar
    else:
        calendar = Calendar.objects.create(name=str(object), slug=slugify(str(object)))
        calendar.create_relation(object)

    return calendar


class Event(Event):
    class Meta:
        proxy = True
