from rest_framework import serializers
from sportapp.models import Register, RegisterUserCampaign


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        #fields = ['id', 'client_id']
        fields='__all__'


# modified by chaitu----
class RegisterUserCampaignSerializer(serializers.ModelSerializer):
    register = serializers.SerializerMethodField()

    class Meta:
        model = RegisterUserCampaign
        fields = ['object_status', 'ref_code', 'campaign_code', 'campaign', 'register']

    def get_register(self, obj):
        return "{}-{}".format(str(obj.register.client_id), obj.register.uname)