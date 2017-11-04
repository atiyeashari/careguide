from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class BabySitter(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    mobile_phone = models.CharField(null=True, max_length=10, blank=True, help_text='4168804341')


class Family(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    mobile_phone = models.CharField(null=True, max_length=10, blank=True, help_text='4168804341')


class TimeSpan(models.Model):
    time_span = models.DurationField()

    class Meta:
        abstract = True


class BookedTime(TimeSpan):
    family = models.ForeignKey(BabySitter)
    baby_sitter = models.ForeignKey(Family)


class Availability(TimeSpan):
    baby_sitter = models.ForeignKey(BabySitter)