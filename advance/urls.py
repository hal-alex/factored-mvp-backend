# from django.urls import (
#     path,
#     include,
# )

# from rest_framework.routers import DefaultRouter

# from advance import views

# router = DefaultRouter()

# router.register('advances', views.AdvanceViewSet)

# app_name = 'advance'

# urlpatterns = [
#     path('', include(router.urls))
# ]

from django.urls import path
from .views import AdvanceListView, AdvanceDetailedView

urlpatterns = [
    path('', AdvanceListView.as_view()),
    path('<pk>/', AdvanceDetailedView.as_view())
]