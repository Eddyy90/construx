from django.db import models
from django.core.validators import RegexValidator
from django.templatetags.static import static


DOCUMENT_TYPE_CHOICES = [
    (0, 'CPF'),
    (1, 'CNPJ'),
]
id_registry_type_field = models.PositiveSmallIntegerField(
    choices=DOCUMENT_TYPE_CHOICES,
    default=0,
)
id_registry_field = models.CharField(max_length=14)
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
phone_number_field = models.CharField(validators=[phone_regex], max_length=17, blank=True)


class CommonProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    phone_number = phone_number_field

    class Meta:
        abstract = True

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static('/images/user_icon.svg')

    @property
    def phone_number_display(self):
        if len(self.phone_number) == 10:
            return '({}{}) {}{}{}{}-{}{}{}{}'.format(*self.phone_number)
        return '({}{}) {}{}{}{}{}-{}{}{}{}'.format(*self.phone_number)


class ClientProfile(CommonProfile):
    social_name = models.CharField(max_length=100, null=True, blank=False)
    initials = models.CharField(max_length=20, null=True, blank=False)
    site_url = models.CharField(max_length=120, null=True, blank=True)
    id_registry_type = id_registry_type_field
    id_registry = id_registry_field
    digital = models.BooleanField(default=False)
    address = models.ForeignKey(
        'address.Address', null=True, blank=False, on_delete=models.CASCADE)
    responsible_name = models.CharField(max_length=100, null=True, blank=False)
    responsible_signature = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return f'{self.social_name}, {self.responsible_name}'


class BaseUserProfile(CommonProfile):
    phone_number = models.CharField(max_length=16)
    id_registry = models.CharField(max_length=11)
    total_access = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name

    @classmethod
    def get_by_client(cls, user):
        if user.is_client:
            client = user.profile
        return cls.objects.filter()


class UserProfile(BaseUserProfile):
    CATEGORY_CHOICES = (
        (0, 'Estagiário'),
        (1, 'Secretário'),
    )
    category = models.IntegerField(
        choices=CATEGORY_CHOICES,
        default=0,
    )