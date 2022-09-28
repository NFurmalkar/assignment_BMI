from rest_framework.serializers import ModelSerializer
from testApp.models import Details
from django.contrib.auth.models import User

class userSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']
