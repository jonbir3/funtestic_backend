from django.conf.urls import url

from children.views import ChildList

urlpatterns = [
    url(r'^get/all', ChildList.as_view(), name='get_all'),
]
