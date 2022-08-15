from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Sum
from datetime import date, datetime
from hr.models import HumanResource


def is_student(user):
    return user.groups.filter(name='Student').exists()


@login_required
def reports(request):
    return render(request, "reports/reports.html")


@login_required
def index(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    context = {}
    hr = HumanResource.objects.get(hr_id=request.user.username)
    context['logged_in_user_profile'] = hr
    return render(request, 'dashboard.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                user_bin = HumanResource.objects.get(hr_id=username).bin
                request.session['bin'] = user_bin.id
                if 'bin' in request.session:
                    print(request.session['bin'])

                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return render(request, 'login.html', {'invalid_login': "Invalid login details given"})
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../login')


def my_custom_page_not_found_view(request, exception):
    return render(request, '404.html')
#
#
# def my_custom_error_view(request):
#     return render(request, '404.html')
#
#
# def my_custom_permission_denied_view(request):
#     return render(request, '404.html')
#
#
# def my_custom_bad_request_view(request):
#     return render(request, '404.html')

