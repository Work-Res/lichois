from rest_framework import serializers
from ...models import ApplicationUser


class ApplicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ("id", "full_name", "user_identifier", "work_location_code", "dob")
