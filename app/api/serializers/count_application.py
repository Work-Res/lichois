from rest_framework import serializers
from app.models import Application

class ApplicationCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
