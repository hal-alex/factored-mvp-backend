from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from addresshistory import views

router = DefaultRouter()

router.register('addresshistories', views.AddressHistoryViewset)

app_name = 'addresshistory'

urlpatterns = [
    path('', include(router.urls))
]