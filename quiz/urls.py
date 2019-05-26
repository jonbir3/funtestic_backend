from django.conf.urls import url
from quiz import views as quiz_views

urlpatterns = [
    url(r'^add/', quiz_views.SaveChildGrade.as_view(), name='save_quiz'),
]

