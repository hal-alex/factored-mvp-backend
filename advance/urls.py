# URL mapping for advance endpoints


from django.urls import path
from .views import (AdvanceListView, 
AdvanceDetailedView, 
AllAdvanceListView, 
ScheduledPaymentView)

urlpatterns = [
    path('advance-payments/<pk>/', ScheduledPaymentView.as_view()),
    path('create/', AdvanceListView.as_view()),
    path('all/', AllAdvanceListView.as_view()),
    path('<pk>/', AdvanceDetailedView.as_view()),
]