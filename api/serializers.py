from rest_framework import serializers

from web.models import User, UserProfile
from data_store import utils


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        producer = utils.get_producer()
        profile_data["user_id"] = user.id
        producer.send('profile-topic', key=b'create', value=profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        producer = utils.get_producer()
        profile_data["user_id"] = instance.id
        producer.send('profile-topic', key=b'update', value=profile_data)
        return instance
