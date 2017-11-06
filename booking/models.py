from django.contrib.auth.models import User, Permission
from django.db import models

# Create your models here.


class BabySitter(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    phone_number = models.CharField(null=True, max_length=10, blank=True, help_text='4168804341')

    def save(self, *args, **kwargs):
        user = self.user
        p = Permission.objects.get(codename='baby_sitter')
        user.user_permissions.add(p)
        super(BabySitter, self).save(*args, **kwargs)

    class Meta:
        permissions = (
            ("baby_sitter", "Can add availabilities"),
        )


class Family(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    phone_number = models.CharField(null=True, max_length=10, blank=True, help_text='4168804341')

    def save(self, *args, **kwargs):
        user = self.user
        p = Permission.objects.get(codename='family')
        user.user_permissions.add(p)
        super(Family, self).save(*args, **kwargs)

    class Meta:
        permissions = (
            ("family", "Can book time spans"),
        )


class TimeSpan(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        abstract = True


class Availability(TimeSpan):
    baby_sitter = models.ForeignKey(BabySitter)


class BookedTime(TimeSpan):
    family = models.ForeignKey(Availability)
    baby_sitter = models.ForeignKey(Family)