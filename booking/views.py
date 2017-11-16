from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
# from booking.models import *
from booking.helper_methods import *
import pytz
from booking.models import BookedTime

utc=pytz.UTC


# Create your views here.


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
                booking.delete()
                add_availability(availability)
                message = "booking successfully deleted"
                return render(request, 'success.html', {"message": message})
        except ObjectDoesNotExist:
            message = 'This booked time does not exists'
            print(message)
            return render(request, 'success.html', {"message": message})

    return render(request, 'success.html', {"message": "invalid request"})


@permission_required('booking.baby_sitter')
@login_required(login_url='/login/')
def baby_sitter_add_availability(request):
    if request and request.user and request.method == 'POST' and request.POST['from-time'] and request.POST['to-time']:
        try:
            baby_sitter = BabySitter.objects.get(user=request.user)
        except ObjectDoesNotExist:
            context = {"message": "Baby sitter not found"}
            return render(request, 'success.html', context)
        from_time = utc.localize(datetime.strptime(request.POST['from-time'], '%Y-%m-%dT%H:%M'))
        to_time = utc.localize(datetime.strptime(request.POST['to-time'], '%Y-%m-%dT%H:%M'))
        availability = Availability(baby_sitter=baby_sitter, start_time=from_time, end_time=to_time)
        message = add_availability(availability)
        return render(request, 'success.html', {"message": message})
    return render(request, 'success.html', {"message":"invalid request"})


@permission_required('booking.baby_sitter')
@login_required(login_url='/login/')
def delete_availability(request):
    if request and request.user and request.method == 'POST' and request.POST['id']:
        availability_id = request.POST['id']
        try:
            availability = Availability.objects.get(id=availability_id)
        except ObjectDoesNotExist:
            context = {"message": "Baby sitter or availability not found"}
            return render(request, 'success.html', context)
        if availability.baby_sitter.user == request.user:
            availability.delete()
            context = {"message": "Availability successfully deleted"}
            return render(request, 'success.html', context)
    context = {"message": "Invalid request"}
    return render(request, 'success.html', context)



@permission_required('booking.family')
@login_required(login_url='/login/')
def add_booking(request):
    pass
