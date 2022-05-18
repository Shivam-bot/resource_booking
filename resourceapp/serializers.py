from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Resources, BookedResources
from .custom_validations import check_string


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name','last_name','email','mobile_no','password','address','city','state','pincode','country')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if first_name is not None:
            first_name_check = check_string(first_name)
            if first_name_check[0]:
                raise serializers.ValidationError({"first_name": first_name_check[1]})
        if last_name is not None:
            last_name_check = check_string(last_name)
            if last_name_check[0]:
                raise serializers.ValidationError({"last_name": last_name_check[1]})
        return data

    def create(self, validated_data):
        password = make_password(validated_data.get('password'))
        validated_data['password'] = password
        user_data = User.objects.create(**validated_data)
        return user_data


class UserData(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ResourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resources
        exclude = ('created_at', 'updated_at')


class BookedResourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedResources
        exclude = ('created_at', 'updated_at', 'user')

    def validate(self, data):
        resource = data.get('resources')
        quantity = data.get('quantity')
        quantity_available = resource.quantity_available
        if not quantity <= quantity_available:
            raise serializers.ValidationError({"quantity": "Quantity not available"})
        return data
