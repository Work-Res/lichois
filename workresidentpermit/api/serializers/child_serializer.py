from rest_framework import serializers
from ...models import Child


class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = (
            "child_first_name",
            "child_last_name",
            "child_age",
            "gender",
            "is_applying_residence"
        )
