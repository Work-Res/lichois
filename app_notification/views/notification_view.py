from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..api.serializers import NotificationSerializer
from ..models import Notification


class NotificationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Optionally, filter notifications by the logged-in user
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Ensure that the user can only access their own notifications
        return Notification.objects.filter(user=self.request.user)

