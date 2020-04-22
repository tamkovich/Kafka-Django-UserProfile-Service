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
        UserProfile.objects.create(user=user, **profile_data)
        producer = utils.get_producer()
        profile_data["user_id"] = user.id
        producer.send('user-topic', key=b'create', value=validated_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        producer = utils.get_producer()
        profile = instance.profile
        profile.update(profile_data, with_commit=True)
        producer.send('user-topic', key=b'update', value=validated_data)
        return instance
