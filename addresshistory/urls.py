from django.urls import path
from .views import AddressHistoryListView, AddressHistoryDetailView

urlpatterns = [
    path('', AddressHistoryListView.as_view()),
    path('<pk>/', AddressHistoryDetailView.as_view())
]