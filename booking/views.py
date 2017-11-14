from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from booking.models import *
from booking.helper_methods import *


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


@login_required(login_url='/login/')
def delete_booking(request):
    if request and request.user and request.method == 'POST' and request.POST['id']:
        booking_id = request.POST['id']
        user = request.user
        try:
            booking = BookedTime.objects.get(id=booking_id)
            if booking.baby_sitter.user == user or booking.family.user == user:
                availability = Availability(baby_sitter=booking.baby_sitter, start_time=booking.start_time, end_time=booking.end_time)
                add_availability(booking.baby_sitter, availability)
                booking.delete()
        except:
            print('This booked time does not exists')

    return render(request, 'familyAccount.html')