from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from booking.models import *


# Create your views here.
from booking.models import BookedTime


@login_required(login_url='/login/')
def index(request):
    if request and request.user:
        if request.user.has_perm('booking.baby_sitter'):
            baby_sitter = BabySitter.objects.get(user=request.user)
            booked_times = BookedTime.objects.filter(baby_sitter=baby_sitter)
            availabilities = Availability.objects.filter(baby_sitter=baby_sitter)
            context = {'bookings': booked_times, 'availabilities': availabilities}
            return render(request, 'babySitterAccount.html', context)
        elif request.user.has_perm('booking.family'):
            context = {}
            return render(request, 'familyAccount.html', context)

    return HttpResponse("Hello, world. You're at the booking index.")
