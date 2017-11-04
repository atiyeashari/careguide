from django.contrib import admin
from booking.models import *

# Register your models here.
admin.site.register(BabySitter)
admin.site.register(Family)
admin.site.register(BookedTime)
admin.site.register(Availability)