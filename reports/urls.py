from django.conf.urls import url
from reports import views as reports_view

urlpatterns = [
    url(r'^sendReport/', reports_view.SendReportToEmail.as_view(), name='send_report'),
    url(r'^save/', reports_view.ReportList.as_view(), name='get_all'),
]


