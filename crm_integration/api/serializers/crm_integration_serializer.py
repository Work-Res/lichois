from rest_framework import serializers

def create_model_serializer(model_cls):
    class ModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_cls
            fields = "__all__"

    return ModelSerializer
