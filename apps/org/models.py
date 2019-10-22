from django.db import models
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.conf import settings
from datetime import datetime


class Org(models.Model):
    name = models.CharField("Operation name", max_length=80)
    address1 = models.CharField('Address 1', max_length=50)
    address2 = models.CharField('Address 2', max_length=50, blank=True, null=True)
    town = models.CharField('Town', max_length=30, blank=True, null=True)
    postcode = models.CharField('Postcode', max_length=10)
    country = models.CharField('Country Code', max_length=3)
    phone = models.CharField(max_length=30)
    website = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, editable=False, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='OrgUser')

    PAYMENT_METHOD_CHOICES = (
        ('b', 'bank transfer'),
        ('l', 'bank transfer, letter of credit accepted')
    )
    # payment_method = models.CharField(blank=True, null=True, choices=PAYMENT_METHOD_CHOICES)
    # hourly_cost = models.IntegerField(blank=True, null=True, verbose_name="Hourly staff cost (in Euro or equivalent)")
    # avg_monthly_salary = models.IntegerField(blank=True, null=True, verbose_name="Average montly salary (in Euro)")

    def is_editable_by(self, user):
        if user in self.users.all() or user.is_staff:
            return True
        return False

    def slug(self):
        s = slugify(self.name)
        if self.town:
            s = '%s-%s' % (s, slugify(self.town))
        return s

    def get_absolute_url(self):
        return f'/{self.slug()}+{self.pk}'

    def get_edit_url(self):
        return f'/edit/{self.pk}'

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_org'
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'


class OrgUser(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)
    created_at = models.DateTimeField(default=datetime.now, editable=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(OrgUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Supplier Account User'
        verbose_name_plural = 'Supplier Account Users'
