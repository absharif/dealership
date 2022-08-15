from django.shortcuts import render
from .models import HumanResource
from django.contrib.auth.decorators import login_required
from bin.models import BIN


@login_required
def hr_list(request):
    try:
        bin = BIN.objects.get(id=request.session['bin'])
    except BIN.DoesNotExist:
        bin = None

    try:
        hr = HumanResource.objects.filter(bin=bin)
    except HumanResource.DoesNotExist:
        hr = None

    return render(request, "hr/hr_list.html", {'hr_list': hr})
