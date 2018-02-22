from rest_framework import serializers

from common.models.terraform_file import TerraformFile
from common.models.environment import Environment


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'terraform_file', )
        read_only_fields = ('id', 'created_at', 'updated_at', )

    def create(self, validated_data):
        return Environment(**validated_data).save()
