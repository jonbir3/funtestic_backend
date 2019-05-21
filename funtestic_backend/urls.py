"""funtestic_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views as users_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(('users.urls', 'users'), namespace='users')),
    url(r'^reports/', include(('reports.urls', 'reports'), namespace='reports')),
    url(r'^children/', include(('children.urls', 'children'), namespace='children')),
    url(r'^quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),
    url(r'^register/', users_views.Register.as_view(), name='register'),
    url(r'^login/', users_views.Login.as_view(), name='login'),
    url(r'^2fa/', users_views.TwoFA.as_view(), name='2fa'),
]
