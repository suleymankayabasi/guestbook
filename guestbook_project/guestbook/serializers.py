from rest_framework import serializers
from .models import User, Entry

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'created_date']

class EntrySerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Entry
        fields = ['id', 'user', 'subject', 'message', 'created_date']