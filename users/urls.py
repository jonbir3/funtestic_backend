from django.conf.urls import url
from . import views as users_view

urlpatterns = [
    url(r'^get/', users_view.ParentDetail.as_view(), name='get_parent_details'),
]
