from notifications.base.models import AbstractNotification


def get_notification_link(obj, notification):
    if hasattr(obj, 'supress_link_from_notifications'):
        if obj.supress_link_from_notifications:
            return None

    if hasattr(obj, 'get_notification_link'):
        ret = obj.get_notification_link(notification)
        if ret:
            return ret

    if hasattr(obj, 'get_absolute_url'):
        return obj.get_absolute_url()

    return None


class Notification(AbstractNotification):

    class Meta(AbstractNotification.Meta):
        abstract = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        link = get_notification_link(self.target, self)
        self.data = {'link': link}

    @property
    def link(self):
        if self.data:
            return self.data.get('link')
