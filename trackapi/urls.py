from django.urls import path
from trackapi.views import FedexTrackingView

urlpatterns = [
    path("track/", FedexTrackingView.as_view(), name='track-it')
]