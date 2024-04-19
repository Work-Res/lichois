from django.urls import path

from .views import GeneratePDFView

urlpatterns = [
    path('pdf/',  GeneratePDFView.as_view()),
]
