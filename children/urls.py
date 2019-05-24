from django.conf.urls import url

from children import views as children_view

urlpatterns = [
    url(r'^get/all/', children_view.ChildList.as_view(), name='get_all'),
    url(r'^add/', children_view.AddChild.as_view(), name='add_child'),
]
