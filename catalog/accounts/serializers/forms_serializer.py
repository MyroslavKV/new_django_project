from django.contrib.auth.models import User
from rest_framework import serializers

class CaptchaFieldSerializer(serializers.Serializer):
    captcha_0 = serializers.CharField
    captcha_1 = serializers.CharField

    def validate(self, attrs):
        from captcha.models import CaptchaStore

        try:
            captcha = CaptchaStore.objects.get(hashkey=attrs['captcha_0'])
        
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError('Incorrect captcha')
        
        if captcha.responce != attrs.get('captcha_1', '').lower():
            raise serializers.ValidationError('Incorrect captcha')

        captcha.delete()
        return attrs

class RegisterFormSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    captcha = CaptchaFieldSerializer(required=True)

    # class Meta:
    #     model = User
    #     extra_fields = ['email']
    #     fields = ['username', 'password1', 'password2']

