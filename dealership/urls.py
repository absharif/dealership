from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),

    path('hr/', include('hr.urls')),
    path('account/', include('account.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

