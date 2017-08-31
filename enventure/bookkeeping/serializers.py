from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
import models
from users.models import User
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value




class AccountSerializer(serializers.ModelSerializer):




    class Meta:
        model = models.Account


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('_image')




    class Meta:
        model = models.Item

    def save(self):
        tm = super(ItemSerializer, self).save()
        return tm

    def _image(self,obj):
        request = self.context.get('request', None)
        if request:
            base = request.build_absolute_uri().rsplit("/",5)[0]
            return base+obj.image.url


class AccountSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = models.Account

class CBOSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
     

    class Meta:
        model = models.Cbo
        fields = ('cboName','phoneNumber','email',"district","address","id")


class EnventureSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
     

    class Meta:
        model = models.Enventure
        fields = ('name','phoneNumber','email','dashboardAccess',"gender","age","id")
class CBODataSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = models.Entry

   
class EntrySerializer(serializers.ModelSerializer):
    _item = serializers.CharField(required=False)
    item = ItemSerializer(read_only=True)
    created_ts = serializers.IntegerField(required=False)


    class Meta:
        model = models.Entry

    


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Device

    def save(self):
        tm = super(DeviceSerializer, self).save()
        return tm


        return fb

class InstallationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Installation

    def save(self):
        tm = super(InstallationSerializer, self).save()
        return tm



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','avatar','karma',"first_name","last_name","name")

    def save(self):
        u = super(UserSerializer, self).save()
        return u

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username']
        )
        user.set_password(validated_data["password"])


        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','email','avatar','mobile','karma',"first_name","last_name","mobile","karma","name",)

    def save(self):
        u = super(UserSerializer, self).save()
        return u

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


