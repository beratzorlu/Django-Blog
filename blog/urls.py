from . import views
from django.urls import path

urlpatterns = [
    # must add as_view due to class-based view structure.
    path('', views.PostList.as_view(), name='home')
]
