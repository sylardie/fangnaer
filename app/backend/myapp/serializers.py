from rest_framework import serializers
from backend.myapp.models import Things


class ThingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Things
        fields = ('__all__')
