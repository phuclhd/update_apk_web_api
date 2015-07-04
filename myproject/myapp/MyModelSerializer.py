from rest_framework import serializers
from myproject.myapp.models import Document
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('packagename', 'version')