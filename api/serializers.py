from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from . import models

class RegistrationSerializer(serializers.ModelSerializer):
    password_1 = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password]
    )
    password_2 = serializers.CharField(
        write_only = True,
        required = True,
    )
    class Meta:
        model = models.CustomUser
        fields = [
            'id',
            'email', 
            'first_name',
            'last_name',
            'description', 
            'gender',
            'dob',
            'blood_group', 
            'present_address', 
            'permanent_address', 
            'phone_number',
            'donor',
            'profile_picture',
            'is_active',
            'password_1',
            'password_2'
        ]
        extra_kwargs = {
            'email' : {'required' : True},
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'description' : {'required' : False},
            'gender' : {'required' : False},
            'dob' : {'required' : False},
            'blood_group' : {'required' : True},
            'present_address' : {'required' : False},
            'permanent_address' : {'required' : False},
            'phone_number' : {'required' : True},
            'is_active' : {'read_only' : True},
        }

    def validate(self, attrs):
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        user = models.CustomUser.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            description = validated_data.get('description', ''),
            gender = validated_data.get('gender', ''),
            dob = validated_data.get('dob', None),
            blood_group = validated_data['blood_group'],
            present_address = validated_data.get('present_address', ''),
            permanent_address = validated_data.get('permanent_address', ''),
            phone_number = validated_data['phone_number'],
            password = validated_data['password_1'],
            profile_picture=validated_data.get('profile_picture')
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = [
            'id',
            'email', 
            'first_name',
            'last_name',
            'description', 
            'gender',
            'dob',
            'blood_group', 
            'present_address', 
            'permanent_address', 
            'phone_number',
            'donor',
            'profile_picture',
            'is_active',
        ]
        extra_kwargs = {
            'email' : {'read_only' : True},
            'first_name' : {'required' : True},
            'last_name' : {'required' : True},
            'description' : {'required' : False},
            'gender' : {'required' : False},
            'dob' : {'required' : False},
            'blood_group' : {'required' : True},
            'present_address' : {'required' : False},
            'permanent_address' : {'required' : False},
            'phone_number' : {'required' : True},
            'is_active' : {'read_only' : True},
        }

class BloodRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BloodRequest
        fields = [
            'id', 
            'patient', 
            'blood_group', 
            'quantity', 
            'description', 
            'location', 
            'date_time', 
            'is_active'
        ]
        extra_kwargs = {
            'patient' : {'read_only' : True},
            'blood_group' : {'read_only' : True},
            'description' : {'required' : False},
        }