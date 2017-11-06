from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request and request.user:
        if request.user.has_perm('booking.baby_sitter'):
            context = {}
            return render(request, 'babySitterAccount.html', context)
        elif request.user.has_perm('booking.family'):
            context = {}
            return render(request, 'familyAccount.html', context)

    return HttpResponse("Hello, world. You're at the booking index.")
