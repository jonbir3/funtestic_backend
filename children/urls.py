from django.conf.urls import url

from children.views import childList

urlpatterns = [
    url(r'^get/all', childList.as_view(), name='get_all'),
]
