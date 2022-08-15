from django.urls import path
from . import views

urlpatterns = [
    path('hr_list/', views.hr_list, name='hr_list'),

]
