from rest_framework import serializers
from users.models import Person
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class PersonSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    def create(self, validated_data):
        user_data = dict(validated_data.pop('user'))
        user_data['username'] = validated_data['phone_number']
        user = User(**user_data)
        user.set_password(user_data['password'])
        person = Person(user=user, phone_number=validated_data['phone_number'])
        person.save()
        return person

    class Meta:
        model = Person
        fields = ('user', 'phone_number')
