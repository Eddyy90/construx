from django.core.management import call_command
from construx.celery import app
from celery.schedules import crontab
from celery import Celery


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 seconds.
    sender.add_periodic_task(10.0, send_notification_emails, name='send notification emails')

    Celery()
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        check_document_due_dates,
    )

@app.task
def send_notification_emails():
    call_command('send_notification_emails')

@app.task
def check_document_due_dates():
    call_command('check_due_processes.py')