import logging
from email.utils import format_datetime

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django_tenants.utils import tenant_context

from clients.models import Client, Domain
from user_notifications.models import Notification


class Command(BaseCommand):
    help = 'Sends emails for notifications.'

    def add_arguments(self, parser):
        parser.add_argument('forever', nargs='?', type=bool)

    def handle(self, *args, **options):
        # Ensure this process doesn't run multiple times concurrently.
        # Lock(die=True).forever()
        self.send_tenant_emails()

    def send_tenant_emails(self):
        for tenant in Client.objects.all():
            if tenant.is_public:
                continue
            with tenant_context(tenant):
                self.send_new_emails()

    def send_new_emails(self):
        # Find notifications that have not been emailed but should be emailed.
        notifications = Notification.objects.filter(
            emailed=False,
        ).order_by('id')

        for notification in notifications:
            self.send_it_out(notification)

    def send_it_out(self, notification):
        target = notification.target

        # Make this transaction atomic
        # Re-check the database to make sure the individual notification is still unsent
        # Lock the notification record in the database while sending the email
        with transaction.atomic():
            notif_latest = Notification.objects.select_for_update().get(
                id=notification.id
            )

            if notif_latest.emailed:
                notif_latest.save()
                return

            link = notification.link
            if link:
                domain = Domain.get_current().domain
                link = f'https://{domain}{link}'

            user = notification.recipient
            subject = "Email de notificação"
            email_template_name = "user_notifications/email.html"
            context = {
                "email": user.email,
                "domain": settings.SITE_URL,
                "site_name": settings.SITE_NAME,
                "user": user,
                "protocol": "https",
                "notification": notification,
                "notification_link": link,
            }
            html_message = render_to_string(email_template_name, context)
            plain_message = strip_tags(html_message)
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email="notifications@construx.io",
                    recipient_list=[user.email],
                    fail_silently=False,
                    html_message=html_message,
                )
            except BadHeaderError as error:
                logging.error(f"Error while sending email: {error}")
                return

            # Mark notification as sent.
            notif_latest.emailed = True
            notif_latest.save(update_fields=['emailed'])
