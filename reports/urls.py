from django.conf.urls import url
from reports import views as reports_view

urlpatterns = [
    url(r'^add/', reports_view.ReportList.as_view(), name='get_all'),

]
