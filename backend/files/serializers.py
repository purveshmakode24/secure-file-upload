from rest_framework import serializers
from core.models import File
from django.utils.translation import gettext_lazy as _


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'file']

    def create(self, validated_data):
        file = validated_data['file']

        x = File.objects.filter(file= file)
        if x.count() > 0:
            msg = _('File with the same name exists.')
            raise serializers.ValidationError(msg)

        return super().create(validated_data)
